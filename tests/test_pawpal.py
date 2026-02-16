"""
Tests for PawPal+ system
"""

import pytest
from datetime import date, timedelta
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


# ============================================================================
# SORTING CORRECTNESS TESTS
# ============================================================================

def test_sort_by_time_chronological_order():
    """Test that tasks are sorted in chronological order by scheduled_time"""
    # Create owner and pet
    owner = Owner("Test Owner", available_time_minutes=120)
    pet = Pet("Buddy", "Dog", 5)
    owner.add_pet(pet)

    # Add tasks OUT OF ORDER
    pet.add_task(Task("Afternoon walk", TaskType.WALK, 20, priority=4, scheduled_time="14:30"))
    pet.add_task(Task("Morning walk", TaskType.WALK, 25, priority=5, scheduled_time="07:00"))
    pet.add_task(Task("Evening walk", TaskType.WALK, 20, priority=3, scheduled_time="18:00"))
    pet.add_task(Task("Feed breakfast", TaskType.FEEDING, 10, priority=5, scheduled_time="07:30"))

    # Create scheduler and sort
    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()

    # Verify tasks are in chronological order
    assert sorted_tasks[0].scheduled_time == "07:00"
    assert sorted_tasks[1].scheduled_time == "07:30"
    assert sorted_tasks[2].scheduled_time == "14:30"
    assert sorted_tasks[3].scheduled_time == "18:00"

    # Verify task names match expected order
    assert sorted_tasks[0].name == "Morning walk"
    assert sorted_tasks[1].name == "Feed breakfast"
    assert sorted_tasks[2].name == "Afternoon walk"
    assert sorted_tasks[3].name == "Evening walk"


def test_sort_by_time_with_no_scheduled_time():
    """Test that tasks without scheduled_time are placed at the end"""
    owner = Owner("Test Owner", available_time_minutes=120)
    pet = Pet("Buddy", "Dog", 5)
    owner.add_pet(pet)

    # Add tasks with and without scheduled times
    pet.add_task(Task("Walk", TaskType.WALK, 20, priority=5, scheduled_time="14:00"))
    pet.add_task(Task("Unscheduled task", TaskType.ENRICHMENT, 15, priority=3, scheduled_time=""))
    pet.add_task(Task("Feed", TaskType.FEEDING, 10, priority=5, scheduled_time="08:00"))

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()

    # Verify scheduled tasks come first
    assert sorted_tasks[0].scheduled_time == "08:00"
    assert sorted_tasks[1].scheduled_time == "14:00"
    # Unscheduled task should be last
    assert sorted_tasks[2].scheduled_time == ""


def test_sort_by_time_empty_list():
    """Test sorting when there are no tasks"""
    owner = Owner("Test Owner", available_time_minutes=120)
    pet = Pet("Buddy", "Dog", 5)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()

    # Should return empty list
    assert len(sorted_tasks) == 0


# ============================================================================
# RECURRENCE LOGIC TESTS
# ============================================================================

def test_daily_task_creates_next_occurrence():
    """Test that marking a daily task complete creates a new task for tomorrow"""
    owner = Owner("Test Owner", available_time_minutes=120)
    pet = Pet("Buddy", "Dog", 5)
    owner.add_pet(pet)

    # Create a daily task with today's date
    today = date.today()
    task = Task(
        "Morning walk",
        TaskType.WALK,
        30,
        priority=5,
        frequency="daily",
        scheduled_time="07:00",
        due_date=today
    )
    pet.add_task(task)

    # Initially should have 1 task
    assert len(pet.get_tasks()) == 1
    assert pet.get_tasks()[0].is_completed == False

    # Mark task as completed
    task.mark_completed()

    # Should now have 2 tasks: original (completed) + new occurrence
    assert len(pet.get_tasks()) == 2

    # First task should be completed
    assert pet.get_tasks()[0].is_completed == True
    assert pet.get_tasks()[0].due_date == today

    # Second task should be incomplete and due tomorrow
    assert pet.get_tasks()[1].is_completed == False
    assert pet.get_tasks()[1].due_date == today + timedelta(days=1)
    assert pet.get_tasks()[1].name == "Morning walk"  # Same name


def test_weekly_task_creates_next_occurrence():
    """Test that marking a weekly task complete creates a new task for next week"""
    owner = Owner("Test Owner", available_time_minutes=120)
    pet = Pet("Buddy", "Dog", 5)
    owner.add_pet(pet)

    # Create a weekly task
    today = date.today()
    task = Task(
        "Vet appointment",
        TaskType.VET_VISIT,
        60,
        priority=4,
        frequency="weekly",
        scheduled_time="14:00",
        due_date=today
    )
    pet.add_task(task)

    # Mark task as completed
    task.mark_completed()

    # Should now have 2 tasks
    assert len(pet.get_tasks()) == 2

    # New task should be due next week (7 days later)
    next_occurrence = pet.get_tasks()[1]
    assert next_occurrence.due_date == today + timedelta(weeks=1)
    assert next_occurrence.is_completed == False


def test_onetime_task_no_recurrence():
    """Test that one-time tasks do not create new occurrences"""
    owner = Owner("Test Owner", available_time_minutes=120)
    pet = Pet("Buddy", "Dog", 5)
    owner.add_pet(pet)

    # Create a one-time task
    task = Task(
        "Special grooming",
        TaskType.GROOMING,
        45,
        priority=3,
        frequency="once",
        scheduled_time="10:00"
    )
    pet.add_task(task)

    # Initially 1 task
    assert len(pet.get_tasks()) == 1

    # Mark task as completed
    task.mark_completed()

    # Should still have only 1 task (no new occurrence)
    assert len(pet.get_tasks()) == 1
    assert pet.get_tasks()[0].is_completed == True


def test_recurring_task_preserves_properties():
    """Test that recurring tasks preserve all properties in new occurrence"""
    owner = Owner("Test Owner", available_time_minutes=120)
    pet = Pet("Buddy", "Dog", 5)
    owner.add_pet(pet)

    # Create task with specific properties
    today = date.today()
    original_task = Task(
        "Morning walk",
        TaskType.WALK,
        30,
        priority=5,
        frequency="daily",
        scheduled_time="07:00",
        due_date=today
    )
    pet.add_task(original_task)
    original_task.mark_completed()

    # Get the new occurrence
    new_task = pet.get_tasks()[1]

    # Verify all properties are preserved (except due_date and is_completed)
    assert new_task.name == original_task.name
    assert new_task.task_type == original_task.task_type
    assert new_task.duration_minutes == original_task.duration_minutes
    assert new_task.priority == original_task.priority
    assert new_task.frequency == original_task.frequency
    assert new_task.scheduled_time == original_task.scheduled_time

    # But due_date should be updated and is_completed should be False
    assert new_task.due_date == today + timedelta(days=1)
    assert new_task.is_completed == False


# ============================================================================
# CONFLICT DETECTION TESTS
# ============================================================================

def test_conflict_detection_overlapping_times_same_pet():
    """Test that Scheduler detects conflicts when tasks overlap for same pet"""
    owner = Owner("Test Owner", available_time_minutes=120)
    pet = Pet("Buddy", "Dog", 5)
    owner.add_pet(pet)

    # Add two overlapping tasks
    # Task 1: 07:00 - 07:30 (30 minutes)
    pet.add_task(Task("Morning walk", TaskType.WALK, 30, priority=5, scheduled_time="07:00"))
    # Task 2: 07:15 - 07:30 (15 minutes) - OVERLAPS with Task 1
    pet.add_task(Task("Feed breakfast", TaskType.FEEDING, 15, priority=5, scheduled_time="07:15"))

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    # Should detect 1 conflict
    assert len(conflicts) == 1
    assert "Morning walk" in conflicts[0]
    assert "Feed breakfast" in conflicts[0]
    assert "07:00" in conflicts[0]
    assert "07:15" in conflicts[0]


def test_conflict_detection_overlapping_times_different_pets():
    """Test that Scheduler detects conflicts across different pets"""
    owner = Owner("Test Owner", available_time_minutes=120)
    dog = Pet("Max", "Dog", 5)
    cat = Pet("Luna", "Cat", 3)
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Add overlapping tasks for different pets
    # Dog walk: 14:00 - 14:25 (25 minutes)
    dog.add_task(Task("Afternoon walk", TaskType.WALK, 25, priority=4, scheduled_time="14:00"))
    # Cat play: 14:10 - 14:30 (20 minutes) - OVERLAPS
    cat.add_task(Task("Play session", TaskType.ENRICHMENT, 20, priority=3, scheduled_time="14:10"))

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    # Should detect 1 conflict
    assert len(conflicts) == 1
    assert "Afternoon walk" in conflicts[0]
    assert "Play session" in conflicts[0]
    assert "Max" in conflicts[0]
    assert "Luna" in conflicts[0]


def test_conflict_detection_no_conflicts():
    """Test that Scheduler returns empty list when no conflicts exist"""
    owner = Owner("Test Owner", available_time_minutes=120)
    pet = Pet("Buddy", "Dog", 5)
    owner.add_pet(pet)

    # Add non-overlapping tasks
    pet.add_task(Task("Morning walk", TaskType.WALK, 30, priority=5, scheduled_time="07:00"))
    pet.add_task(Task("Feed breakfast", TaskType.FEEDING, 10, priority=5, scheduled_time="08:00"))
    pet.add_task(Task("Afternoon walk", TaskType.WALK, 25, priority=4, scheduled_time="14:00"))

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    # Should have no conflicts
    assert len(conflicts) == 0


def test_conflict_detection_adjacent_tasks():
    """Test that adjacent tasks (end time = start time) do not conflict"""
    owner = Owner("Test Owner", available_time_minutes=120)
    pet = Pet("Buddy", "Dog", 5)
    owner.add_pet(pet)

    # Task 1: 07:00 - 07:30
    pet.add_task(Task("Morning walk", TaskType.WALK, 30, priority=5, scheduled_time="07:00"))
    # Task 2: 07:30 - 07:40 (starts exactly when Task 1 ends)
    pet.add_task(Task("Feed breakfast", TaskType.FEEDING, 10, priority=5, scheduled_time="07:30"))

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    # Adjacent tasks should not conflict
    assert len(conflicts) == 0


def test_conflict_detection_multiple_conflicts():
    """Test detection of multiple overlapping conflicts"""
    owner = Owner("Test Owner", available_time_minutes=120)
    pet = Pet("Buddy", "Dog", 5)
    owner.add_pet(pet)

    # Create multiple overlapping tasks around 07:00
    pet.add_task(Task("Task 1", TaskType.WALK, 30, priority=5, scheduled_time="07:00"))  # 07:00-07:30
    pet.add_task(Task("Task 2", TaskType.FEEDING, 20, priority=5, scheduled_time="07:15"))  # 07:15-07:35
    pet.add_task(Task("Task 3", TaskType.ENRICHMENT, 15, priority=4, scheduled_time="07:20"))  # 07:20-07:35

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    # Should detect 3 conflicts: (1,2), (1,3), (2,3)
    assert len(conflicts) == 3


def test_conflict_detection_ignores_completed_tasks():
    """Test that conflict detection only checks incomplete tasks"""
    owner = Owner("Test Owner", available_time_minutes=120)
    pet = Pet("Buddy", "Dog", 5)
    owner.add_pet(pet)

    # Add overlapping tasks (non-recurring to avoid auto-creation)
    task1 = Task("Morning walk", TaskType.WALK, 30, priority=5,
                 scheduled_time="07:00", frequency="once")
    task2 = Task("Feed breakfast", TaskType.FEEDING, 15, priority=5,
                 scheduled_time="07:15", frequency="once")

    pet.add_task(task1)
    pet.add_task(task2)

    # Before marking complete, should have 1 conflict
    scheduler = Scheduler(owner)
    conflicts_before = scheduler.detect_conflicts()
    assert len(conflicts_before) == 1

    # Mark first task as completed
    task1.mark_completed()

    # After marking complete, should have no conflicts (task1 is now completed)
    conflicts_after = scheduler.detect_conflicts()
    assert len(conflicts_after) == 0


def test_get_conflicts_report_format():
    """Test that get_conflicts_report returns properly formatted string"""
    owner = Owner("Test Owner", available_time_minutes=120)
    pet = Pet("Buddy", "Dog", 5)
    owner.add_pet(pet)

    # Test with no conflicts
    scheduler = Scheduler(owner)
    report = scheduler.get_conflicts_report()
    assert "✅" in report
    assert "No scheduling conflicts" in report

    # Add conflicting tasks
    pet.add_task(Task("Task 1", TaskType.WALK, 30, priority=5, scheduled_time="07:00"))
    pet.add_task(Task("Task 2", TaskType.FEEDING, 15, priority=5, scheduled_time="07:15"))

    report = scheduler.get_conflicts_report()
    assert "SCHEDULING CONFLICTS DETECTED" in report
    assert "⚠️ CONFLICT" in report
