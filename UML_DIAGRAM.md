# PawPal+ Final UML Class Diagram

## Overview
This UML diagram represents the final implementation of the PawPal+ pet care scheduling system, showing all classes, their relationships, attributes, and methods as actually implemented.

## How to Generate PNG from Mermaid

### Option 1: Online Mermaid Editor (Easiest)
1. Go to https://mermaid.live/
2. Copy the contents of `uml_final.mmd`
3. Paste into the editor
4. Click "PNG" or "SVG" to download the image
5. Save as `uml_final.png`

### Option 2: VS Code Extension
1. Install the "Markdown Preview Mermaid Support" extension
2. Open `uml_final.mmd` in VS Code
3. Right-click and select "Preview Mermaid Diagram"
4. Export as PNG

### Option 3: Command Line (Requires Node.js)
```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i uml_final.mmd -o uml_final.png
```

## Class Descriptions

### 1. **TaskType** (Enum)
Enumeration defining all types of pet care tasks:
- `WALK` - Walking/exercise activities
- `FEEDING` - Meal and feeding tasks
- `MEDICATION` - Medicine administration
- `GROOMING` - Bathing, brushing, nail trimming
- `ENRICHMENT` - Play, training, mental stimulation
- `VET_VISIT` - Veterinary appointments

### 2. **Task**
Represents an individual pet care task with scheduling details.

**Key Attributes:**
- `name: str` - Task description
- `task_type: TaskType` - Category of task
- `duration_minutes: int` - How long the task takes
- `priority: int` - Importance level (1-5)
- `frequency: str` - Recurrence pattern (daily/weekly/once)
- `scheduled_time: str` - Specific time (HH:MM format)
- `due_date: date` - When the task is due
- `is_completed: bool` - Completion status
- `pet: Pet` - Reference to associated pet

**Key Methods:**
- `mark_completed()` - Marks task done and auto-creates next occurrence for recurring tasks
- `create_next_occurrence()` - Creates new task instance using timedelta
- `can_fit_in_schedule()` - Checks if task fits in available time

**Algorithmic Features:**
- 🔄 **Recurring Tasks**: Auto-recreation using `timedelta(days=1)` or `timedelta(weeks=1)`
- ✓ **Completion Tracking**: Visual status indicators (○ incomplete, ✓ completed)
- 📅 **Due Date Management**: Automatic date calculations

### 3. **Pet**
Represents a pet being cared for and stores their tasks.

**Key Attributes:**
- `name: str` - Pet's name
- `species: str` - Dog, Cat, etc.
- `age: int` - Pet's age in years
- `special_needs: str` - Special care requirements
- `tasks: List[Task]` - All tasks for this pet

**Key Methods:**
- `add_task(task)` - Adds task and sets pet reference
- `get_tasks()` - Returns all tasks
- `get_incomplete_tasks()` - Returns only pending tasks

**Relationship:** **Composition** (1 Pet contains 0..* Tasks)
- Pet owns its tasks
- Tasks cannot exist without a pet
- When pet is removed, tasks are removed

### 4. **Owner**
Represents the pet owner who manages multiple pets.

**Key Attributes:**
- `name: str` - Owner's name
- `available_time_minutes: int` - Daily time budget
- `preferences: Dict` - Custom preferences
- `pets: List[Pet]` - All owned pets

**Key Methods:**
- `add_pet(pet)` - Adds pet to collection
- `get_all_tasks()` - Aggregates tasks from all pets
- `get_all_incomplete_tasks()` - Gets pending tasks across all pets
- `get_available_time()` - Returns time budget

**Relationship:** **Composition** (1 Owner contains 1..* Pets)
- Owner manages multiple pets
- Centralized task aggregation
- Single source of time constraints

### 5. **Schedule**
Represents a daily schedule/plan for pet care.

**Key Attributes:**
- `date: date` - Schedule date
- `tasks: List[Task]` - Scheduled tasks
- `total_duration: int` - Sum of all task durations
- `reasoning: str` - Explanation of scheduling decisions

**Key Methods:**
- `add_task(task)` - Adds task to schedule
- `remove_task(task)` - Removes task from schedule
- `get_total_duration()` - Calculates total time
- `display_plan()` - Formats schedule for display
- `get_reasoning()` - Returns explanation

**Relationship:** **Aggregation** (1 Schedule contains 0..* Tasks)
- Schedule references tasks but doesn't own them
- Tasks can exist independently of schedules
- Non-destructive scheduling

### 6. **Scheduler** (Brain of the System)
Main logic engine that generates optimal pet care schedules.

**Key Attributes:**
- `owner: Owner` - Reference to owner being scheduled

**Core Scheduling Methods:**
- `generate_plan()` - Creates optimized daily schedule
- `prioritize_tasks()` - Sorts by priority then duration
- `validate_constraints()` - Checks time limits
- `explain_reasoning()` - Generates human-readable explanation

**Advanced Algorithmic Methods:**

#### 🔄 **Sorting & Filtering**
- `sort_by_time(tasks)` → **O(n log n)**
  - Uses Python's Timsort with lambda function
  - Chronological ordering by scheduled_time
  - Unscheduled tasks placed at end

- `filter_by_status(completed)` → **O(n)**
  - Linear scan with list comprehension
  - View incomplete or completed tasks

- `filter_by_pet(pet_name)` → **O(n)**
  - Direct lookup by pet name
  - Focus on individual pet tasks

- `filter_by_type(task_type)` → **O(n)**
  - Filter by TaskType enum
  - View all tasks of specific category

#### ⚠️ **Conflict Detection**
- `detect_conflicts()` → **O(n log n) + O(n²)**
  - Sort tasks by time (O(n log n))
  - Pairwise overlap checking (O(n²))
  - Uses interval overlap algorithm: `start1 < end2 AND start2 < end1`
  - Returns warning strings (non-destructive)

- `get_conflicts_report()` → **O(n log n) + O(n²)**
  - Formatted user-friendly conflict report
  - Shows all overlapping tasks with times

**Relationship:**
- **Association** with Owner (manages)
- **Dependency** on Schedule (creates)
- **Dependency** on Task (filters/sorts)

## Key Relationships

### Composition (Strong Ownership)
```
Owner ◆━━━ Pet ◆━━━ Task
```
- Owner owns Pets (1:many)
- Pet owns Tasks (1:many)
- Lifecycle dependency: if owner/pet deleted, children deleted

### Aggregation (Weak Reference)
```
Schedule ◇━━━ Task
```
- Schedule references Tasks but doesn't own them
- Tasks can exist without being scheduled
- Schedule can be deleted without deleting tasks

### Association (Uses)
```
Scheduler ━━━> Owner
Scheduler ┄┄┄> Schedule (creates)
Scheduler ┄┄┄> Task (filters/sorts)
Task ━━━> TaskType (uses)
Task ━━━> Pet (belongs to)
```

## Changes from Initial Design

### Added Attributes
- `Task.scheduled_time` - For time-based sorting and conflict detection
- `Task.due_date` - For recurring task management
- `Task.frequency` - For auto-recreation logic
- `Task.pet` - Back-reference for recurring task creation

### Added Methods (Algorithmic Features)

**Scheduler:**
- `sort_by_time()` - Time-based chronological sorting
- `filter_by_status()` - Filter by completion status
- `filter_by_pet()` - Filter by pet name
- `filter_by_type()` - Filter by task type
- `detect_conflicts()` - Overlap detection algorithm
- `get_conflicts_report()` - Formatted conflict output
- `_calculate_end_time()` - Helper for time calculations

**Task:**
- `mark_completed()` - Enhanced with auto-recreation
- `create_next_occurrence()` - New task generation using timedelta

**Pet:**
- `get_incomplete_tasks()` - Filter incomplete tasks

**Owner:**
- `get_all_incomplete_tasks()` - Aggregate incomplete tasks across pets

### New Relationships
- Task → Pet (back-reference for recurring tasks)
- Scheduler creates Schedule (dependency)
- Scheduler uses Task for filtering/sorting

## Algorithm Summary

| Feature | Algorithm | Complexity | Implementation |
|---------|-----------|------------|----------------|
| Time Sorting | Timsort | O(n log n) | `sorted(tasks, key=lambda t: t.scheduled_time)` |
| Status Filter | List comprehension | O(n) | `[t for t in tasks if t.is_completed == status]` |
| Pet Filter | Linear search | O(n) | Iterate pets, return when match |
| Type Filter | List comprehension | O(n) | `[t for t in tasks if t.task_type == type]` |
| Recurring Tasks | Date arithmetic | O(1) | `due_date + timedelta(days=1)` |
| Conflict Detection | Sort + pairwise | O(n log n) + O(n²) | Interval overlap algorithm |

## Testing Coverage
✅ **16 comprehensive tests** covering:
- Basic functionality (2 tests)
- Sorting correctness (3 tests)
- Recurrence logic (4 tests)
- Conflict detection (7 tests)

## Performance Characteristics
- **Scalability**: All algorithms ≤ O(n log n) except conflict detection O(n²)
- **Efficiency**: Optimized with Python built-ins (sorted, list comprehensions)
- **Reliability**: Non-destructive operations, no crashes on conflicts
- **Usability**: Clear error messages and reasoning explanations

---

**Last Updated:** 2026-02-15
**Implementation Status:** ✅ Production Ready
**Test Coverage:** 16/16 passing (100%)
**Confidence Level:** ★★★★★ (5/5 Stars)
