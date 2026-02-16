"""
Main script for PawPal+ system demonstration
"""

from pawpal_system import Pet, Owner, Task, TaskType, Scheduler


def main():
    # Create an Owner
    owner = Owner("Jordan", available_time_minutes=90)

    # Create two Pets
    dog = Pet("Max", "Dog", 3)
    cat = Pet("Luna", "Cat", 2)

    # Add pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Add tasks to the dog (at least 3 tasks with different times)
    dog.add_task(Task("Morning walk", TaskType.WALK, 25, priority=5))
    dog.add_task(Task("Feed breakfast", TaskType.FEEDING, 10, priority=5))
    dog.add_task(Task("Afternoon walk", TaskType.WALK, 20, priority=4))
    dog.add_task(Task("Training session", TaskType.ENRICHMENT, 15, priority=3))

    # Add tasks to the cat (at least 3 tasks with different times)
    cat.add_task(Task("Feed breakfast", TaskType.FEEDING, 5, priority=5))
    cat.add_task(Task("Play with toys", TaskType.ENRICHMENT, 10, priority=3))
    cat.add_task(Task("Brush fur", TaskType.GROOMING, 8, priority=2))

    # Create scheduler and generate plan
    scheduler = Scheduler(owner)
    schedule = scheduler.generate_plan()

    # Print "Today's Schedule"
    print("\n" + "=" * 60)
    print("TODAY'S SCHEDULE - PawPal+")
    print("=" * 60)
    print()
    print(schedule.display_plan())
    print("=" * 60)


if __name__ == "__main__":
    main()
