"""Tests for the PawPal+ logic layer."""

import os
import sys

# Make the project root importable when running pytest from anywhere.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pawpal_system import Owner, Pet, Task, TaskType


def test_mark_complete_changes_status():
    """Calling mark_complete() should flip a task's status to completed."""
    task = Task("morning walk", TaskType.WALK, duration=30, priority=4)
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    """Adding a task to a Pet should increase that pet's task count by one."""
    rex = Pet(name="Rex", kind="dog")
    assert len(rex.tasks) == 0

    rex.add_task(Task("give meds", TaskType.MEDS, duration=5, priority=9))

    assert len(rex.tasks) == 1
