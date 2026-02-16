"""
Test script for recurring task functionality
Demonstrates automatic task recreation when daily/weekly tasks are completed
"""

from datetime import date, timedelta
from pawpal_system import Pet, Owner, Task, TaskType, Scheduler


def main():
    print("\n" + "=" * 70)
    print("TESTING RECURRING TASKS - PawPal+")
    print("=" * 70)

    # Create owner and pet
    owner = Owner("Sarah", available_time_minutes=120)
    dog = Pet("Buddy", "Dog", 4)
    owner.add_pet(dog)

    # Add recurring tasks (daily and weekly)
    print("\n1. Adding recurring tasks...")
    print("-" * 70)

    today = date.today()
    dog.add_task(Task(
        "Morning walk",
        TaskType.WALK,
        30,
        priority=5,
        frequency="daily",
        scheduled_time="07:00",
        due_date=today
    ))

    dog.add_task(Task(
        "Feed breakfast",
        TaskType.FEEDING,
        10,
        priority=5,
        frequency="daily",
        scheduled_time="07:30",
        due_date=today
    ))

    dog.add_task(Task(
        "Vet appointment",
        TaskType.VET_VISIT,
        60,
        priority=4,
        frequency="weekly",
        scheduled_time="14:00",
        due_date=today
    ))

    # Add a one-time task (not recurring)
    dog.add_task(Task(
        "Special grooming",
        TaskType.GROOMING,
        45,
        priority=3,
        frequency="once",
        scheduled_time="10:00",
        due_date=today
    ))

    # Display initial tasks
    print(f"\nInitial tasks (Due: {today}):")
    for task in dog.get_tasks():
        print(f"  {task}")

    # Test 1: Mark a daily task complete
    print("\n2. Marking 'Morning walk' (daily) as complete...")
    print("-" * 70)
    morning_walk = dog.get_tasks()[0]
    morning_walk.mark_completed()

    print(f"\n✓ Task marked complete. A new occurrence should be created for tomorrow.")
    print(f"\nAll tasks after completing 'Morning walk':")
    for task in dog.get_tasks():
        print(f"  {task}")

    # Test 2: Mark a weekly task complete
    print("\n3. Marking 'Vet appointment' (weekly) as complete...")
    print("-" * 70)
    vet_task = [t for t in dog.get_tasks() if t.name == "Vet appointment" and not t.is_completed][0]
    vet_task.mark_completed()

    print(f"\n✓ Task marked complete. A new occurrence should be created for next week.")
    print(f"\nAll tasks after completing 'Vet appointment':")
    for task in dog.get_tasks():
        print(f"  {task}")

    # Test 3: Mark a one-time task complete
    print("\n4. Marking 'Special grooming' (once) as complete...")
    print("-" * 70)
    special_task = [t for t in dog.get_tasks() if t.name == "Special grooming"][0]
    special_task.mark_completed()

    print(f"\n✓ Task marked complete. No new occurrence should be created (one-time task).")
    print(f"\nAll tasks after completing 'Special grooming':")
    for task in dog.get_tasks():
        print(f"  {task}")

    # Display summary by due date
    print("\n5. Summary of tasks by due date:")
    print("-" * 70)

    # Group tasks by due date
    tasks_by_date = {}
    for task in dog.get_tasks():
        if task.due_date not in tasks_by_date:
            tasks_by_date[task.due_date] = []
        tasks_by_date[task.due_date].append(task)

    # Display grouped by date
    for due_date in sorted(tasks_by_date.keys()):
        print(f"\nDue on {due_date}:")
        for task in tasks_by_date[due_date]:
            print(f"  {task}")

    # Test filtering incomplete tasks
    print("\n6. Filtering incomplete tasks only:")
    print("-" * 70)
    incomplete_tasks = dog.get_incomplete_tasks()
    print(f"Found {len(incomplete_tasks)} incomplete task(s):")
    for task in incomplete_tasks:
        print(f"  {task}")

    print("\n" + "=" * 70)
    print("RECURRING TASKS TEST COMPLETE!")
    print("=" * 70)
    print("\nKey observations:")
    print("- Daily tasks create new instances for tomorrow (today + 1 day)")
    print("- Weekly tasks create new instances for next week (today + 7 days)")
    print("- One-time tasks do NOT create new instances when completed")
    print("- Completed tasks remain in the list with ✓ status")
    print("- timedelta() is used to calculate next due dates accurately")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
