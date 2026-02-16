"""
PawPal+ System Classes
Module 2 Project - Pet Care Task Planning System
"""

from enum import Enum
from datetime import date, timedelta, datetime, time
from typing import List, Dict, Optional, Tuple


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
        task.pet = self  # Set reference to this pet
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
                 priority: int, frequency: str = "daily", scheduled_time: str = "",
                 due_date: date = None):
        """Initialize a Task instance"""
        self.name = name
        self.task_type = task_type
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.frequency = frequency
        self.is_completed = False
        self.scheduled_time = scheduled_time  # Format: "HH:MM" (e.g., "08:00", "14:30")
        self.due_date = due_date if due_date else date.today()  # Default to today
        self.pet = None  # Will be set when task is added to a pet

    def mark_completed(self) -> None:
        """Mark this task as completed and auto-create next occurrence if recurring.

        Sets the is_completed flag to True, which changes the task's display
        status from ○ to ✓. For recurring tasks (daily or weekly frequency),
        automatically creates a new task instance for the next occurrence and
        adds it to the pet's task list.

        This automatic recreation ensures that routine tasks like daily walks
        or weekly grooming don't need to be manually recreated by the pet owner.

        Behavior:
        - Always sets is_completed = True
        - If frequency is "daily": Creates new task for tomorrow
        - If frequency is "weekly": Creates new task for next week
        - One-time tasks: No new task created
        - Completed task remains in list for historical tracking

        Example:
            >>> task = Task("Morning walk", TaskType.WALK, 30, priority=5,
            ...             frequency="daily", due_date=date(2026, 2, 15))
            >>> dog.add_task(task)
            >>> print(len(dog.get_tasks()))
            1
            >>> task.mark_completed()
            >>> print(len(dog.get_tasks()))  # Now has 2 tasks
            2
            >>> print(dog.get_tasks()[0].is_completed)
            True
            >>> print(dog.get_tasks()[1].due_date)
            2026-02-16  # Tomorrow!

        Note:
            The task must be associated with a pet (self.pet must be set) for
            automatic recreation to work. This happens automatically when using
            pet.add_task().
        """
        self.is_completed = True

        # Handle recurring tasks
        if self.frequency.lower() in ["daily", "weekly"] and self.pet:
            next_task = self.create_next_occurrence()
            self.pet.add_task(next_task)

    def create_next_occurrence(self) -> 'Task':
        """Create a new task instance for the next occurrence using timedelta.

        Helper method for recurring task management. Creates a brand new Task
        object with all the same properties (name, type, duration, priority, etc.)
        but with an updated due_date calculated using Python's timedelta.

        This method is called automatically by mark_completed() for recurring tasks
        and should not typically be called directly by user code.

        Date Calculation:
        - "daily" frequency: due_date + timedelta(days=1) → tomorrow
        - "weekly" frequency: due_date + timedelta(weeks=1) → next week (7 days)
        - Other frequencies: due_date unchanged (for custom handling)

        Algorithm: O(1) constant time
        Uses: datetime.timedelta for accurate date arithmetic

        Returns:
            New Task instance with identical properties except updated due_date.
            The new task is NOT automatically added to any pet - that's handled
            by mark_completed().

        Example:
            >>> task = Task("Morning walk", TaskType.WALK, 30, priority=5,
            ...             frequency="daily", due_date=date(2026, 2, 15))
            >>> next_task = task.create_next_occurrence()
            >>> print(next_task.due_date)
            2026-02-16
            >>> print(next_task.name)
            Morning walk
            >>> print(next_task.is_completed)
            False  # New task starts as incomplete

        Note:
            timedelta automatically handles month and year rollovers.
            For example, January 31 + 1 day = February 1.
        """
        # Calculate next due date using timedelta
        if self.frequency.lower() == "daily":
            next_due = self.due_date + timedelta(days=1)
        elif self.frequency.lower() == "weekly":
            next_due = self.due_date + timedelta(weeks=1)  # or timedelta(days=7)
        else:
            next_due = self.due_date  # Default to same date for other frequencies

        # Create new task instance with same properties but new due date
        return Task(
            name=self.name,
            task_type=self.task_type,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            scheduled_time=self.scheduled_time,
            due_date=next_due
        )

    def can_fit_in_schedule(self, available_time: int) -> bool:
        """Check if task can fit within available time"""
        return self.duration_minutes <= available_time

    def __str__(self) -> str:
        """Return string representation of the task"""
        status = "✓" if self.is_completed else "○"
        time_str = f" @ {self.scheduled_time}" if self.scheduled_time else ""
        due_str = f" [Due: {self.due_date}]" if self.due_date else ""
        freq_str = f" ({self.frequency})" if self.frequency != "daily" else ""
        return f"{status} {self.name} ({self.task_type.value}) - {self.duration_minutes}min{time_str}{due_str} [Priority: {self.priority}]{freq_str}"


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

    def sort_by_time(self, tasks: List[Task] = None) -> List[Task]:
        """Sort tasks by scheduled time in chronological order (HH:MM format).

        Uses Python's built-in sorted() function with a lambda key function
        to sort tasks by their scheduled_time attribute. Tasks without a
        scheduled time are automatically placed at the end of the sorted list.

        Algorithm: Timsort (O(n log n) time complexity)
        Lambda function: key=lambda t: t.scheduled_time if t.scheduled_time else "99:99"

        Args:
            tasks: Optional list of tasks to sort. If None, sorts all owner's tasks.

        Returns:
            List of Task objects sorted by scheduled_time in ascending order.

        Example:
            >>> scheduler = Scheduler(owner)
            >>> sorted_tasks = scheduler.sort_by_time()
            >>> for task in sorted_tasks:
            ...     print(f"{task.scheduled_time}: {task.name}")
            07:00: Morning walk
            08:00: Feed breakfast
            14:30: Afternoon walk
        """
        if tasks is None:
            tasks = self.owner.get_all_tasks()

        # Sort by scheduled_time; tasks without time go to the end
        return sorted(tasks, key=lambda t: t.scheduled_time if t.scheduled_time else "99:99")

    def filter_by_status(self, completed: bool = False) -> List[Task]:
        """Filter tasks by completion status using list comprehension.

        Uses a list comprehension to efficiently filter tasks based on their
        is_completed attribute. This is useful for viewing only tasks that
        still need to be done or reviewing completed tasks.

        Algorithm: Linear scan (O(n) time complexity)
        Implementation: List comprehension with boolean filter

        Args:
            completed: If True, return completed tasks (marked with ✓);
                      If False, return incomplete tasks (marked with ○).
                      Defaults to False.

        Returns:
            List of Task objects matching the specified completion status.

        Example:
            >>> scheduler = Scheduler(owner)
            >>> incomplete = scheduler.filter_by_status(completed=False)
            >>> print(f"You have {len(incomplete)} tasks to complete")
            You have 5 tasks to complete
            >>> completed = scheduler.filter_by_status(completed=True)
            >>> print(f"You completed {len(completed)} tasks today!")
            You completed 3 tasks today!
        """
        all_tasks = self.owner.get_all_tasks()
        return [task for task in all_tasks if task.is_completed == completed]

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Filter tasks by pet name for focused task management.

        Searches through the owner's pets to find a pet with the matching name
        and returns all tasks associated with that pet. This is useful for
        managing tasks for individual pets in multi-pet households.

        Algorithm: Linear search (O(n) time complexity where n is number of pets)
        Implementation: Iterate through pets, return tasks when name matches

        Args:
            pet_name: Name of the pet to filter by (case-sensitive string).

        Returns:
            List of Task objects belonging to the specified pet.
            Returns empty list if no pet with that name is found.

        Example:
            >>> scheduler = Scheduler(owner)
            >>> max_tasks = scheduler.filter_by_pet("Max")
            >>> print(f"Max has {len(max_tasks)} tasks:")
            Max has 4 tasks:
            >>> for task in max_tasks:
            ...     print(f"  - {task.name}")
              - Morning walk
              - Feed breakfast
              - Afternoon walk
              - Training session
        """
        for pet in self.owner.pets:
            if pet.name == pet_name:
                return pet.get_tasks()
        return []

    def filter_by_type(self, task_type: TaskType) -> List[Task]:
        """Filter tasks by task type (walk, feeding, medication, etc.).

        Uses a list comprehension to filter all tasks across all pets based on
        their task_type attribute. This is useful for viewing all tasks of a
        specific category, such as all walks or all feeding times.

        Algorithm: Linear scan (O(n) time complexity where n is total tasks)
        Implementation: List comprehension with enum comparison

        Args:
            task_type: TaskType enum value to filter by (e.g., TaskType.WALK,
                      TaskType.FEEDING, TaskType.MEDICATION, etc.).

        Returns:
            List of Task objects matching the specified task type across all pets.

        Example:
            >>> scheduler = Scheduler(owner)
            >>> walks = scheduler.filter_by_type(TaskType.WALK)
            >>> print(f"Total walks scheduled: {len(walks)}")
            Total walks scheduled: 3
            >>> feeding_tasks = scheduler.filter_by_type(TaskType.FEEDING)
            >>> total_feeding_time = sum(t.duration_minutes for t in feeding_tasks)
            >>> print(f"Total feeding time: {total_feeding_time} minutes")
            Total feeding time: 15 minutes
        """
        all_tasks = self.owner.get_all_tasks()
        return [task for task in all_tasks if task.task_type == task_type]

    def detect_conflicts(self) -> List[str]:
        """Detect scheduling conflicts for tasks with overlapping time intervals.

        Uses a lightweight overlap detection algorithm to identify tasks that
        are scheduled at conflicting times. This prevents double-booking and
        helps owners identify scheduling issues before they become problems.

        Algorithm: Sort + Pairwise Comparison
        - Time Complexity: O(n log n) for sorting + O(n²) for pairwise checks
        - Space Complexity: O(n) for storing sorted tasks
        - Overlap Formula: start1 < end2 AND start2 < end1

        The algorithm:
        1. Filters tasks that have scheduled times
        2. Sorts tasks by scheduled_time (O(n log n))
        3. Compares each pair of tasks for time overlaps (O(n²))
        4. Calculates end times: end_time = start_time + duration
        5. Returns warning messages (non-destructive, doesn't crash)

        Returns:
            List of warning message strings describing each conflict found.
            Empty list if no conflicts detected.
            Format: "⚠️ CONFLICT: 'Task1' (Pet1) at HH:MM overlaps with 'Task2' (Pet2) at HH:MM"

        Example:
            >>> scheduler = Scheduler(owner)
            >>> conflicts = scheduler.detect_conflicts()
            >>> if conflicts:
            ...     print("Found conflicts:")
            ...     for conflict in conflicts:
            ...         print(f"  {conflict}")
            Found conflicts:
              ⚠️ CONFLICT: 'Morning walk' (Max) at 07:00 overlaps with 'Feed breakfast' (Max) at 07:15
              ⚠️ CONFLICT: 'Vet visit' (Max) at 14:00 overlaps with 'Play session' (Luna) at 14:10

        Note:
            This method only checks incomplete tasks. Completed tasks are excluded
            from conflict detection since they've already been done.
        """
        warnings = []
        tasks = self.owner.get_all_incomplete_tasks()

        # Filter tasks that have scheduled times
        scheduled_tasks = [t for t in tasks if t.scheduled_time]

        # Sort by scheduled time for efficient detection (O(n log n))
        sorted_tasks = sorted(scheduled_tasks, key=lambda t: t.scheduled_time)

        # Check each pair of adjacent tasks for overlaps
        for i in range(len(sorted_tasks)):
            for j in range(i + 1, len(sorted_tasks)):
                task1 = sorted_tasks[i]
                task2 = sorted_tasks[j]

                # Parse scheduled times (HH:MM format)
                if task1.scheduled_time and task2.scheduled_time:
                    start1_str = task1.scheduled_time
                    start2_str = task2.scheduled_time

                    # Calculate end times by adding duration
                    end1 = self._calculate_end_time(start1_str, task1.duration_minutes)
                    end2 = self._calculate_end_time(start2_str, task2.duration_minutes)

                    # Check for overlap: start1 < end2 AND start2 < end1
                    if start1_str < end2 and start2_str < end1:
                        # Found a conflict!
                        pet1_name = task1.pet.name if task1.pet else "Unknown"
                        pet2_name = task2.pet.name if task2.pet else "Unknown"

                        warning = (
                            f"⚠️ CONFLICT: '{task1.name}' ({pet1_name}) at {start1_str} "
                            f"overlaps with '{task2.name}' ({pet2_name}) at {start2_str}"
                        )
                        warnings.append(warning)

        return warnings

    def _calculate_end_time(self, start_time: str, duration_minutes: int) -> str:
        """Calculate end time by adding duration to start time using timedelta.

        Helper method for conflict detection. Converts HH:MM string to datetime,
        adds duration using timedelta, then formats back to HH:MM string.
        Automatically handles hour rollovers (e.g., 23:50 + 20 minutes = 00:10).

        Algorithm: String parsing + datetime arithmetic + formatting
        Time Complexity: O(1) constant time
        Uses: datetime.timedelta for accurate time arithmetic

        Args:
            start_time: Start time in HH:MM format (24-hour, e.g., "14:30").
            duration_minutes: Task duration in minutes (e.g., 30).

        Returns:
            End time in HH:MM format (24-hour).

        Example:
            >>> scheduler = Scheduler(owner)
            >>> end = scheduler._calculate_end_time("07:00", 30)
            >>> print(end)
            07:30
            >>> end = scheduler._calculate_end_time("14:45", 25)
            >>> print(end)
            15:10
            >>> end = scheduler._calculate_end_time("23:50", 20)  # Hour rollover
            >>> print(end)
            00:10
        """
        # Parse start time
        hours, minutes = map(int, start_time.split(':'))

        # Create datetime for calculation
        start_dt = datetime(2000, 1, 1, hours, minutes)
        end_dt = start_dt + timedelta(minutes=duration_minutes)

        # Format as HH:MM
        return end_dt.strftime("%H:%M")

    def get_conflicts_report(self) -> str:
        """Generate a formatted, user-friendly report of all scheduling conflicts.

        Wraps the detect_conflicts() method to provide a nicely formatted report
        suitable for display to users. Returns either a success message if no
        conflicts exist, or a numbered list of all conflicts found.

        This method provides a non-destructive way to check for scheduling issues
        without raising exceptions or stopping program execution.

        Returns:
            Formatted string with either:
            - Success message: "✅ No scheduling conflicts detected!" (no conflicts)
            - Conflict report: Numbered list of all conflicts with decorative borders

        Example:
            >>> scheduler = Scheduler(owner)
            >>> print(scheduler.get_conflicts_report())
            SCHEDULING CONFLICTS DETECTED:
            ============================================================
            1. ⚠️ CONFLICT: 'Morning walk' (Max) at 07:00 overlaps with 'Feed breakfast' (Max) at 07:15
            2. ⚠️ CONFLICT: 'Vet visit' (Max) at 14:00 overlaps with 'Play session' (Luna) at 14:10
            ============================================================

            >>> # Or if no conflicts:
            >>> print(scheduler.get_conflicts_report())
            ✅ No scheduling conflicts detected!

        Note:
            This is the recommended method for checking conflicts in user-facing
            code as it provides clear, readable output.
        """
        conflicts = self.detect_conflicts()

        if not conflicts:
            return "✅ No scheduling conflicts detected!"

        report = "SCHEDULING CONFLICTS DETECTED:\n"
        report += "=" * 60 + "\n"
        for i, conflict in enumerate(conflicts, 1):
            report += f"{i}. {conflict}\n"
        report += "=" * 60
        return report
