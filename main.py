"""Testing ground for the PawPal+ logic layer.

Builds a small owner/pet/task scenario and prints today's schedule.
Run with: python main.py
"""

from pawpal_system import Owner, Pet, Task, TaskType, Scheduler


def main() -> None:
    # 1. Create an owner with a daily time budget (in minutes).
    owner = Owner(name="Sam", available_minutes=60)

    # 2. Create at least two pets.
    rex = Pet(name="Rex", kind="dog")
    mia = Pet(name="Mia", kind="cat")
    owner.add_pet(rex)
    owner.add_pet(mia)

    # 3. Add at least three tasks with different durations and priorities.
    rex.add_task(Task("morning walk", TaskType.WALK, duration=30, priority=4))
    rex.add_task(Task("give meds", TaskType.MEDS, duration=5, priority=9))
    mia.add_task(Task("feed", TaskType.FEEDING, duration=10, priority=8))
    mia.add_task(Task("grooming session", TaskType.GROOMING, duration=40, priority=2))

    # 4. Build and print today's schedule.
    scheduler = Scheduler(owner.all_tasks(), owner.available_minutes, owner.preferences)
    plan = scheduler.build_plan(date="2026-06-23")

    print("=" * 40)
    print("Today's Schedule")
    print("=" * 40)
    print(plan.explain_choices())


if __name__ == "__main__":
    main()
