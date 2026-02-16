"""
Test script for conflict detection functionality
Demonstrates lightweight conflict detection for overlapping scheduled tasks
"""

from datetime import date
from pawpal_system import Pet, Owner, Task, TaskType, Scheduler


def main():
    print("\n" + "=" * 70)
    print("TESTING CONFLICT DETECTION - PawPal+")
    print("=" * 70)

    # Create owner and pets
    owner = Owner("Emma", available_time_minutes=180)
    dog = Pet("Charlie", "Dog", 5)
    cat = Pet("Mittens", "Cat", 3)

    owner.add_pet(dog)
    owner.add_pet(cat)

    today = date.today()

    # Scenario 1: No conflicts - tasks at different times
    print("\n1. Testing tasks with NO conflicts (different times):")
    print("-" * 70)

    dog.add_task(Task(
        "Morning walk",
        TaskType.WALK,
        30,
        priority=5,
        scheduled_time="07:00",
        due_date=today
    ))

    cat.add_task(Task(
        "Feed breakfast",
        TaskType.FEEDING,
        10,
        priority=5,
        scheduled_time="08:00",
        due_date=today
    ))

    dog.add_task(Task(
        "Afternoon walk",
        TaskType.WALK,
        25,
        priority=4,
        scheduled_time="14:00",
        due_date=today
    ))

    scheduler = Scheduler(owner)
    print(scheduler.get_conflicts_report())

    # Scenario 2: Add conflicting tasks (same pet)
    print("\n2. Testing SAME PET conflicts:")
    print("-" * 70)

    # Add a task that overlaps with Morning walk (07:00-07:30)
    dog.add_task(Task(
        "Feed breakfast",
        TaskType.FEEDING,
        15,
        priority=5,
        scheduled_time="07:15",  # Conflicts with morning walk!
        due_date=today
    ))

    print(scheduler.get_conflicts_report())

    # Scenario 3: Add conflicting tasks (different pets)
    print("\n3. Testing DIFFERENT PETS conflicts:")
    print("-" * 70)

    # Add a cat task that conflicts with dog's afternoon walk (14:00-14:25)
    cat.add_task(Task(
        "Play session",
        TaskType.ENRICHMENT,
        20,
        priority=3,
        scheduled_time="14:10",  # Conflicts with dog's afternoon walk!
        due_date=today
    ))

    print(scheduler.get_conflicts_report())

    # Scenario 4: Multiple overlapping conflicts
    print("\n4. Testing MULTIPLE conflicts:")
    print("-" * 70)

    # Add more conflicting tasks
    dog.add_task(Task(
        "Training",
        TaskType.ENRICHMENT,
        30,
        priority=3,
        scheduled_time="14:05",  # Another conflict at 14:00 time slot!
        due_date=today
    ))

    cat.add_task(Task(
        "Brush fur",
        TaskType.GROOMING,
        20,
        priority=2,
        scheduled_time="07:20",  # Conflicts with 07:00 time slot!
        due_date=today
    ))

    print(scheduler.get_conflicts_report())

    # Display all scheduled tasks
    print("\n5. All scheduled tasks (sorted by time):")
    print("-" * 70)
    sorted_tasks = scheduler.sort_by_time()
    for task in sorted_tasks:
        pet_name = task.pet.name if task.pet else "Unknown"
        duration_end = scheduler._calculate_end_time(
            task.scheduled_time,
            task.duration_minutes
        ) if task.scheduled_time else ""
        time_range = f"{task.scheduled_time}-{duration_end}" if duration_end else "No time"
        print(f"  [{time_range}] {task.name} ({pet_name}) - {task.duration_minutes}min")

    print("\n" + "=" * 70)
    print("CONFLICT DETECTION TEST COMPLETE!")
    print("=" * 70)
    print("\nKey observations:")
    print("- Lightweight algorithm: O(n log n) time complexity (sorting)")
    print("- Overlap detection: start1 < end2 AND start2 < end1")
    print("- Returns warnings instead of crashing")
    print("- Detects conflicts within same pet AND across different pets")
    print("- Useful for preventing double-booking and scheduling errors")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
