"""
PawPal+ System Classes
Module 2 Project - Pet Care Task Planning System
"""

from enum import Enum
from datetime import date
from typing import List, Dict, Optional


class TaskType(Enum):
    """Enumeration of different types of pet care tasks"""
    WALK = "walk"
    FEEDING = "feeding"
    MEDICATION = "medication"
    GROOMING = "grooming"
    ENRICHMENT = "enrichment"
    VET_VISIT = "vet_visit"


class Pet:
    """Represents a pet being cared for and stores their tasks"""

    def __init__(self, name: str, species: str, age: int, special_needs: str = ""):
        """Initialize a Pet instance"""
        self.name = name
        self.species = species
        self.age = age
        self.special_needs = special_needs
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list"""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet"""
        return self.tasks

    def get_incomplete_tasks(self) -> List[Task]:
        """Return only incomplete tasks for this pet"""
        return [task for task in self.tasks if not task.is_completed]

    def __str__(self) -> str:
        """Return string representation of the pet"""
        needs = f" (Special needs: {self.special_needs})" if self.special_needs else ""
        return f"{self.name} - {self.species}, {self.age} years old{needs}"


class Owner:
    """Represents the pet owner who manages multiple pets"""

    def __init__(self, name: str, available_time_minutes: int, preferences: Optional[Dict] = None):
        """Initialize an Owner instance"""
        self.name = name
        self.available_time_minutes = available_time_minutes
        self.preferences = preferences if preferences is not None else {}
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's collection"""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks from all pets"""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def get_all_incomplete_tasks(self) -> List[Task]:
        """Get all incomplete tasks from all pets"""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_incomplete_tasks())
        return all_tasks

    def get_available_time(self) -> int:
        """Return the owner's available time in minutes"""
        return self.available_time_minutes

    def __str__(self) -> str:
        """Return string representation of the owner"""
        pet_count = len(self.pets)
        pet_text = "pet" if pet_count == 1 else "pets"
        return f"{self.name} - {self.available_time_minutes} min available, {pet_count} {pet_text}"


class Task:
    """Represents an individual pet care task"""

    def __init__(self, name: str, task_type: TaskType, duration_minutes: int,
                 priority: int, frequency: str = "daily"):
        """Initialize a Task instance"""
        self.name = name
        self.task_type = task_type
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.frequency = frequency
        self.is_completed = False

    def mark_completed(self) -> None:
        """Mark this task as completed"""
        self.is_completed = True

    def can_fit_in_schedule(self, available_time: int) -> bool:
        """Check if task can fit within available time"""
        return self.duration_minutes <= available_time

    def __str__(self) -> str:
        """Return string representation of the task"""
        status = "✓" if self.is_completed else "○"
        return f"{status} {self.name} ({self.task_type.value}) - {self.duration_minutes}min [Priority: {self.priority}]"


class Schedule:
    """Represents a daily schedule/plan for pet care"""

    def __init__(self, schedule_date: date):
        """Initialize a Schedule instance"""
        self.date = schedule_date
        self.tasks: List[Task] = []
        self.total_duration = 0
        self.reasoning = ""

    def add_task(self, task: Task) -> None:
        """Add a task to the schedule"""
        self.tasks.append(task)
        self.total_duration += task.duration_minutes

    def remove_task(self, task: Task) -> None:
        """Remove a task from the schedule"""
        if task in self.tasks:
            self.tasks.remove(task)
            self.total_duration -= task.duration_minutes

    def get_total_duration(self) -> int:
        """Calculate and return total duration of all tasks"""
        return self.total_duration

    def display_plan(self) -> str:
        """Display the schedule in a readable format"""
        if not self.tasks:
            return f"Schedule for {self.date}: No tasks scheduled"

        plan = f"Schedule for {self.date}:\n"
        plan += f"Total Duration: {self.total_duration} minutes\n"
        plan += "-" * 50 + "\n"
        for i, task in enumerate(self.tasks, 1):
            plan += f"{i}. {task}\n"
        if self.reasoning:
            plan += "-" * 50 + "\n"
            plan += f"Reasoning: {self.reasoning}\n"
        return plan

    def get_reasoning(self) -> str:
        """Return the reasoning behind this schedule"""
        return self.reasoning


class Scheduler:
    """Main logic engine that generates optimal pet care schedules across all pets"""

    def __init__(self, owner: Owner):
        """Initialize a Scheduler instance"""
        self.owner = owner

    def generate_plan(self) -> Schedule:
        """Generate an optimal daily schedule based on constraints and priorities"""
        schedule = Schedule(date.today())

        # Get all incomplete tasks from all pets
        all_tasks = self.owner.get_all_incomplete_tasks()

        if not all_tasks:
            schedule.reasoning = "No incomplete tasks to schedule."
            return schedule

        # Prioritize tasks (higher priority first, then by duration)
        prioritized = self.prioritize_tasks()

        # Add tasks to schedule while respecting time constraints
        remaining_time = self.owner.get_available_time()
        scheduled_tasks = []
        skipped_tasks = []

        for task in prioritized:
            if task.can_fit_in_schedule(remaining_time):
                schedule.add_task(task)
                scheduled_tasks.append(task)
                remaining_time -= task.duration_minutes
            else:
                skipped_tasks.append(task)

        # Generate reasoning
        schedule.reasoning = self.explain_reasoning(schedule, skipped_tasks)

        return schedule

    def prioritize_tasks(self) -> List[Task]:
        """Sort and prioritize tasks based on priority (higher first) and duration (shorter first)"""
        all_tasks = self.owner.get_all_incomplete_tasks()
        # Sort by priority (descending), then by duration (ascending)
        return sorted(all_tasks, key=lambda t: (-t.priority, t.duration_minutes))

    def validate_constraints(self, schedule: Schedule) -> bool:
        """Validate that a schedule meets all constraints"""
        total_duration = schedule.get_total_duration()
        available_time = self.owner.get_available_time()
        return total_duration <= available_time

    def explain_reasoning(self, schedule: Schedule, skipped_tasks: List[Task] = None) -> str:
        """Generate explanation for why this schedule was chosen"""
        if skipped_tasks is None:
            skipped_tasks = []

        explanation_parts = []

        # Basic info
        scheduled_count = len(schedule.tasks)
        total_time = schedule.get_total_duration()
        available = self.owner.get_available_time()

        explanation_parts.append(
            f"Scheduled {scheduled_count} task(s) using {total_time}/{available} minutes available."
        )

        # Explain prioritization
        if scheduled_count > 0:
            explanation_parts.append(
                "Tasks were prioritized by importance (higher priority first), "
                "then by duration (shorter tasks first for efficiency)."
            )

        # Explain skipped tasks
        if skipped_tasks:
            explanation_parts.append(
                f"{len(skipped_tasks)} task(s) could not fit in the available time: "
                + ", ".join([t.name for t in skipped_tasks]) + "."
            )

        return " ".join(explanation_parts)
