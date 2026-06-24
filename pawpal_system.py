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
    preferred_time: str | None = None   # e.g. "morning", "evening", or "HH:MM"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        ...


@dataclass
class Pet:
    name: str
    kind: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet."""
        ...


@dataclass
class Owner:
    name: str
    available_minutes: int = 0
    pets: list[Pet] = field(default_factory=list)
    preferences: dict = field(default_factory=dict)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet to this owner."""
        ...

    def set_preference(self, key: str, value) -> None:
        """Record an owner preference used during scheduling."""
        ...

    def all_tasks(self) -> list[Task]:
        """Collect every task across all of this owner's pets."""
        ...


@dataclass
class DailyPlan:
    date: str
    scheduled_tasks: list[Task] = field(default_factory=list)
    skipped_tasks: list[Task] = field(default_factory=list)
    explanation: str = ""

    def explain_choices(self) -> str:
        """Return a human-readable explanation of why the plan looks as it does."""
        ...


class Scheduler:
    """Produces a daily plan from an owner's tasks given time and preference constraints."""

    def __init__(self, tasks: list[Task], time_budget: int, preferences: dict | None = None):
        self.tasks = tasks
        self.time_budget = time_budget
        self.preferences = preferences or {}

    def build_plan(self, date: str) -> DailyPlan:
        """Build and return the daily plan."""
        ...

    def rank_tasks(self) -> list[Task]:
        """Order tasks by priority (and any other ranking rules)."""
        ...

    def _fits_constraints(self, task: Task, used_minutes: int) -> bool:
        """Check whether a task can fit given remaining time and preferences."""
        ...
