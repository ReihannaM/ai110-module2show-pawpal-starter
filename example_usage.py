"""
Example usage of the PawPal+ system
"""

from pawpal_system import Pet, Owner, Task, TaskType, Scheduler
from datetime import date


def main():
    # Create an owner
    owner = Owner("Alex", available_time_minutes=120)

    # Create pets
    dog = Pet("Buddy", "Dog", 5)
    cat = Pet("Whiskers", "Cat", 3, special_needs="Requires medication")

    # Add pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Create tasks for the dog
    dog.add_task(Task("Morning walk", TaskType.WALK, 30, priority=5))
    dog.add_task(Task("Feed breakfast", TaskType.FEEDING, 10, priority=5))
    dog.add_task(Task("Evening walk", TaskType.WALK, 30, priority=4))
    dog.add_task(Task("Play fetch", TaskType.ENRICHMENT, 20, priority=3))

    # Create tasks for the cat
    cat.add_task(Task("Feed breakfast", TaskType.FEEDING, 5, priority=5))
    cat.add_task(Task("Give medication", TaskType.MEDICATION, 5, priority=5))
    cat.add_task(Task("Clean litter box", TaskType.GROOMING, 10, priority=4))
    cat.add_task(Task("Interactive play", TaskType.ENRICHMENT, 15, priority=3))

    # Display owner and pets
    print("=" * 60)
    print(owner)
    print()
    for pet in owner.pets:
        print(pet)
        print(f"  Tasks: {len(pet.get_tasks())}")
    print("=" * 60)
    print()

    # Create scheduler and generate plan
    scheduler = Scheduler(owner)
    schedule = scheduler.generate_plan()

    # Display the schedule
    print(schedule.display_plan())
    print()

    # Validate constraints
    if scheduler.validate_constraints(schedule):
        print("✓ Schedule meets all time constraints")
    else:
        print("✗ Schedule exceeds available time")


if __name__ == "__main__":
    main()
