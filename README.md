# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

PawPal+ includes advanced algorithmic features to make pet care scheduling more efficient:

### 🔄 Recurring Tasks
Tasks automatically recreate themselves when completed:
- **Daily tasks** → Next occurrence created for tomorrow (`timedelta(days=1)`)
- **Weekly tasks** → Next occurrence created for next week (`timedelta(weeks=1)`)
- Completed tasks remain visible with historical tracking
- No manual task recreation needed

### 🔍 Advanced Filtering
Multiple ways to organize and view tasks:
- **By completion status** → View only incomplete or completed tasks
- **By pet name** → See tasks for a specific pet
- **By task type** → Filter walks, feeding, medications, etc.

### ⏰ Time-Based Sorting
Sort tasks chronologically using lambda functions:
- Tasks displayed in time order (HH:MM format)
- Quick view of what's coming up next
- Efficient O(n log n) sorting algorithm

### ⚠️ Conflict Detection
Lightweight overlap detection prevents double-booking:
- Detects tasks scheduled at overlapping times
- Works across same pet or different pets
- Returns warnings instead of crashing
- Uses interval overlap algorithm: `start1 < end2 AND start2 < end1`

### 📊 Performance
All algorithms designed for efficiency:
- Sorting: O(n log n) with Python's Timsort
- Filtering: O(n) linear scans
- Conflict detection: O(n log n) + O(n²) pairwise checks
- Recurring tasks: O(1) constant time recreation

### 🧪 Testing
Run test scripts to see features in action:
```bash
python main.py           # All features demo
python test_recurring.py # Recurring tasks
python test_conflicts.py # Conflict detection
```

For detailed documentation, see:
- `ALGORITHM_IMPROVEMENTS.md` - Complete feature guide
- `RECURRING_TASKS.md` - Recurring task details
