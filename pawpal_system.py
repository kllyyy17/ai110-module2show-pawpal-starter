"""PawPal+ logic layer.

Backend classes for tracking pet care tasks, applying constraints,
and producing an explained daily plan.
"""

from dataclasses import dataclass, field
from enum import Enum


class TaskType(Enum):
    WALK = "walk"
    FEEDING = "feeding"
    MEDS = "meds"
    ENRICHMENT = "enrichment"
    GROOMING = "grooming"


@dataclass
class Task:
    action: str
    type: TaskType
    duration: int          # estimated minutes
    priority: int          # higher = more important
    pet_name: str = ""     # which pet this task is for (set by Pet.add_task)
    preferred_time: str | None = None   # e.g. "morning", "evening", or "HH:MM"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def label(self) -> str:
        """Short human-readable name, e.g. 'walk Rex'."""
        return f"{self.action} {self.pet_name}".strip()


@dataclass
class Pet:
    name: str
    kind: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet, stamping task.pet_name with this pet's name."""
        task.pet_name = self.name
        self.tasks.append(task)


@dataclass
class Owner:
    name: str
    available_minutes: int = 0
    pets: list[Pet] = field(default_factory=list)
    preferences: dict = field(default_factory=dict)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet to this owner."""
        self.pets.append(pet)

    def set_preference(self, key: str, value) -> None:
        """Record an owner preference used during scheduling.

        Recognized keys:
          - "excluded_types": list of TaskType values the owner does not want scheduled
          - "boost": dict mapping a TaskType value -> int added to that task's priority
        """
        self.preferences[key] = value

    def all_tasks(self) -> list[Task]:
        """Collect every (incomplete) task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks if not task.completed]


@dataclass
class DailyPlan:
    date: str
    scheduled_tasks: list[Task] = field(default_factory=list)
    skipped_tasks: list[Task] = field(default_factory=list)
    explanation: str = ""

    def explain_choices(self) -> str:
        """Return a human-readable explanation of why the plan looks as it does."""
        if self.explanation:
            return self.explanation

        lines = [f"Daily plan for {self.date}:"]
        if self.scheduled_tasks:
            lines.append("Scheduled:")
            for t in self.scheduled_tasks:
                lines.append(f"  - {t.label()} (priority {t.priority}, {t.duration} min)")
        else:
            lines.append("Scheduled: nothing fit the available time.")
        if self.skipped_tasks:
            lines.append("Skipped:")
            for t in self.skipped_tasks:
                lines.append(f"  - {t.label()} (priority {t.priority}, {t.duration} min)")
        return "\n".join(lines)


class Scheduler:
    """Produces a daily plan from an owner's tasks given time and preference constraints."""

    def __init__(self, tasks: list[Task], time_budget: int, preferences: dict | None = None):
        """Store the tasks, time budget, and preferences used to build a plan."""
        self.tasks = tasks
        self.time_budget = time_budget
        self.preferences = preferences or {}

    def _effective_priority(self, task: Task) -> int:
        """Task priority adjusted by any owner preference boost for its type."""
        boost = self.preferences.get("boost", {})
        return task.priority + boost.get(task.type.value, 0)

    def rank_tasks(self) -> list[Task]:
        """Order tasks most-important first.

        Sort key: highest effective priority, then shortest duration (quick wins
        break ties), then action name for a stable, deterministic order.
        """
        return sorted(
            self.tasks,
            key=lambda t: (-self._effective_priority(t), t.duration, t.action),
        )

    def _fits_constraints(self, task: Task, used_minutes: int) -> bool:
        """Check whether a task can be added given remaining time and preferences."""
        excluded = self.preferences.get("excluded_types", [])
        if task.type.value in excluded:
            return False
        return used_minutes + task.duration <= self.time_budget

    def build_plan(self, date: str) -> DailyPlan:
        """Greedily fill the time budget with the highest-priority tasks that fit."""
        plan = DailyPlan(date=date)
        used_minutes = 0
        reasons: list[str] = []
        excluded = self.preferences.get("excluded_types", [])

        for task in self.rank_tasks():
            if task.type.value in excluded:
                plan.skipped_tasks.append(task)
                reasons.append(f"Skipped {task.label()}: owner preference excludes {task.type.value} tasks.")
            elif self._fits_constraints(task, used_minutes):
                plan.scheduled_tasks.append(task)
                used_minutes += task.duration
                reasons.append(
                    f"Scheduled {task.label()}: priority {self._effective_priority(task)}, "
                    f"{task.duration} min ({used_minutes}/{self.time_budget} min used)."
                )
            else:
                plan.skipped_tasks.append(task)
                remaining = self.time_budget - used_minutes
                reasons.append(
                    f"Skipped {task.label()}: needs {task.duration} min but only "
                    f"{remaining} min left in the budget."
                )

        header = (
            f"Plan for {date}: scheduled {len(plan.scheduled_tasks)} of "
            f"{len(self.tasks)} tasks using {used_minutes}/{self.time_budget} minutes."
        )
        plan.explanation = "\n".join([header, *reasons])
        return plan
