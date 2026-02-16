"""
Main script for PawPal+ system demonstration
"""

from pawpal_system import Pet, Owner, Task, TaskType, Scheduler


def main():
    # Create an Owner
    owner = Owner("Jordan", available_time_minutes=120)

    # Create two Pets
    dog = Pet("Max", "Dog", 3)
    cat = Pet("Luna", "Cat", 2)

    # Add pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Add tasks OUT OF ORDER with scheduled times
    print("\n" + "=" * 60)
    print("TESTING SORTING AND FILTERING - PawPal+")
    print("=" * 60)

    # Add dog tasks out of chronological order
    dog.add_task(Task("Afternoon walk", TaskType.WALK, 20, priority=4, scheduled_time="14:30"))
    dog.add_task(Task("Morning walk", TaskType.WALK, 25, priority=5, scheduled_time="07:00"))
    dog.add_task(Task("Evening walk", TaskType.WALK, 20, priority=3, scheduled_time="18:00"))
    dog.add_task(Task("Feed breakfast", TaskType.FEEDING, 10, priority=5, scheduled_time="07:30"))
    dog.add_task(Task("Training session", TaskType.ENRICHMENT, 15, priority=3, scheduled_time="10:00"))

    # Add cat tasks out of chronological order
    cat.add_task(Task("Play with toys", TaskType.ENRICHMENT, 10, priority=3, scheduled_time="15:00"))
    cat.add_task(Task("Feed breakfast", TaskType.FEEDING, 5, priority=5, scheduled_time="08:00"))
    cat.add_task(Task("Brush fur", TaskType.GROOMING, 8, priority=2, scheduled_time="20:00"))
    cat.add_task(Task("Give medication", TaskType.MEDICATION, 5, priority=5, scheduled_time="08:30"))

    # Mark some tasks as completed for testing filtering
    dog.get_tasks()[1].mark_completed()  # Morning walk completed
    cat.get_tasks()[1].mark_completed()  # Feed breakfast completed

    # Create scheduler
    scheduler = Scheduler(owner)

    # Test 1: Display all tasks (unsorted)
    print("\n1. ALL TASKS (unsorted, as added):")
    print("-" * 60)
    all_tasks = owner.get_all_tasks()
    for task in all_tasks:
        print(f"  {task}")

    # Test 2: Sort tasks by time using lambda function
    print("\n2. TASKS SORTED BY TIME (using lambda):")
    print("-" * 60)
    sorted_tasks = scheduler.sort_by_time()
    for task in sorted_tasks:
        print(f"  {task}")

    # Test 3: Filter by completion status
    print("\n3. INCOMPLETE TASKS ONLY:")
    print("-" * 60)
    incomplete = scheduler.filter_by_status(completed=False)
    for task in incomplete:
        print(f"  {task}")

    print("\n4. COMPLETED TASKS ONLY:")
    print("-" * 60)
    completed = scheduler.filter_by_status(completed=True)
    for task in completed:
        print(f"  {task}")

    # Test 4: Filter by pet name
    print("\n5. MAX'S TASKS:")
    print("-" * 60)
    max_tasks = scheduler.filter_by_pet("Max")
    for task in max_tasks:
        print(f"  {task}")

    print("\n6. LUNA'S TASKS:")
    print("-" * 60)
    luna_tasks = scheduler.filter_by_pet("Luna")
    for task in luna_tasks:
        print(f"  {task}")

    # Test 5: Filter by task type
    print("\n7. FEEDING TASKS:")
    print("-" * 60)
    feeding_tasks = scheduler.filter_by_type(TaskType.FEEDING)
    for task in feeding_tasks:
        print(f"  {task}")

    print("\n8. WALK TASKS:")
    print("-" * 60)
    walk_tasks = scheduler.filter_by_type(TaskType.WALK)
    for task in walk_tasks:
        print(f"  {task}")

    # Test 9: Conflict detection
    print("\n9. DETECTING SCHEDULING CONFLICTS:")
    print("-" * 60)
    print("\nChecking for overlapping tasks...")
    print(scheduler.get_conflicts_report())

    # Generate optimized schedule
    print("\n" + "=" * 60)
    print("GENERATED OPTIMIZED SCHEDULE:")
    print("=" * 60)
    schedule = scheduler.generate_plan()
    print(schedule.display_plan())
    print("=" * 60)


if __name__ == "__main__":
    main()
