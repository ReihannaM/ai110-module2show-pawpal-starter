# Recurring Tasks Implementation

## Overview
Automatic task recreation for daily and weekly recurring tasks using Python's `timedelta`.

## Features Implemented

### 1. **Automatic Task Recreation**
When a recurring task (daily/weekly) is marked complete, a new instance is automatically created for the next occurrence.

### 2. **Due Date Tracking**
- Each task now has a `due_date` attribute (defaults to today)
- Due dates are calculated using `timedelta`:
  - **Daily**: `due_date + timedelta(days=1)` → tomorrow
  - **Weekly**: `due_date + timedelta(weeks=1)` → next week (7 days)

### 3. **Frequency Types**
- `"daily"` - Creates new instance for next day
- `"weekly"` - Creates new instance for next week
- Other frequencies (e.g., "once") - No automatic recreation

## Implementation Details

### Task Class Changes
```python
# New attributes
self.due_date = due_date if due_date else date.today()
self.pet = None  # Reference to parent pet

# Updated mark_completed()
def mark_completed(self) -> None:
    self.is_completed = True
    if self.frequency.lower() in ["daily", "weekly"] and self.pet:
        next_task = self.create_next_occurrence()
        self.pet.add_task(next_task)

# New method
def create_next_occurrence(self) -> 'Task':
    if self.frequency.lower() == "daily":
        next_due = self.due_date + timedelta(days=1)
    elif self.frequency.lower() == "weekly":
        next_due = self.due_date + timedelta(weeks=1)
    return Task(...)  # Create new instance with next_due
```

### Pet Class Changes
```python
def add_task(self, task: Task) -> None:
    task.pet = self  # Set reference to parent pet
    self.tasks.append(task)
```

## Using timedelta

### Basic Usage
```python
from datetime import date, timedelta

today = date.today()
tomorrow = today + timedelta(days=1)
next_week = today + timedelta(weeks=1)  # or timedelta(days=7)
```

### Key Points
- `timedelta()` represents a duration/difference between two dates
- Can add/subtract days, weeks, hours, minutes, seconds
- Automatically handles month/year rollovers
- Arguments: `days`, `weeks`, `hours`, `minutes`, `seconds`, `microseconds`

## Example Usage

```python
# Create a daily recurring task
task = Task(
    "Morning walk",
    TaskType.WALK,
    30,
    priority=5,
    frequency="daily",
    scheduled_time="07:00",
    due_date=date.today()
)

dog.add_task(task)

# Mark complete - automatically creates new task for tomorrow
task.mark_completed()

# Now dog has 2 tasks:
# ✓ Morning walk (Due: 2026-02-15) - completed
# ○ Morning walk (Due: 2026-02-16) - new instance
```

## Test Results

Running `test_recurring.py` demonstrates:
1. ✅ Daily tasks create next occurrence for tomorrow
2. ✅ Weekly tasks create next occurrence for next week (7 days later)
3. ✅ One-time tasks do NOT create new instances
4. ✅ Completed tasks remain with ✓ status
5. ✅ Due dates are calculated accurately using timedelta

## Benefits for Pet Owners

- **No manual task recreation** - Daily feeding, walks automatically repeat
- **Clear due date tracking** - See when each task is due
- **Historical record** - Completed tasks remain visible
- **Flexible frequencies** - Support daily, weekly, or custom patterns

## Sources

Implementation based on Python datetime documentation:
- [datetime.timedelta() function - GeeksforGeeks](https://www.geeksforgeeks.org/python/python-datetime-timedelta-function/)
- [How to Add or Subtract Days from a Date in Python - Statology](https://www.statology.org/how-to-add-or-subtract-days-from-a-date-in-python/)
- [How to Use datetime.timedelta in Python With Examples - MigueNdes](https://miguendes.me/how-to-use-datetimetimedelta-in-python-with-examples)
- [How to add Days or Weeks to a Date in Python - Bobby Hadz](https://bobbyhadz.com/blog/python-add-days-to-date)
