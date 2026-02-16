"""
Tests for PawPal+ system
"""

import pytest
from pawpal_system import Pet, Owner, Task, TaskType, Scheduler


def test_task_completion():
    """Test that calling mark_completed() changes the task's status"""
    # Create a task
    task = Task("Morning walk", TaskType.WALK, 30, priority=5)

    # Verify task is not completed initially
    assert task.is_completed == False

    # Mark task as completed
    task.mark_completed()

    # Verify task is now completed
    assert task.is_completed == True


def test_task_addition():
    """Test that adding a task to a Pet increases that pet's task count"""
    # Create a pet
    pet = Pet("Buddy", "Dog", 5)

    # Verify pet has 0 tasks initially
    assert len(pet.get_tasks()) == 0

    # Add a task to the pet
    task = Task("Feed breakfast", TaskType.FEEDING, 10, priority=5)
    pet.add_task(task)

    # Verify pet now has 1 task
    assert len(pet.get_tasks()) == 1

    # Add another task
    task2 = Task("Evening walk", TaskType.WALK, 25, priority=4)
    pet.add_task(task2)

    # Verify pet now has 2 tasks
    assert len(pet.get_tasks()) == 2
