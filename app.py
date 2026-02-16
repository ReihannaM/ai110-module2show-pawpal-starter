import streamlit as st
import pandas as pd
from datetime import date
from pawpal_system import Pet, Owner, Task, TaskType, Scheduler, Schedule

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+ Pet Care Scheduler")
st.caption("Smart scheduling for busy pet owners")

# Initialize Owner in session state (only once!)
if 'owner' not in st.session_state:
    st.session_state.owner = Owner("Jordan", available_time_minutes=120)

# Initialize current pet in session state
if 'current_pet' not in st.session_state:
    st.session_state.current_pet = None

with st.expander("ℹ️ About PawPal+", expanded=False):
    st.markdown(
        """
**PawPal+** is an intelligent pet care planning assistant that helps you:
- 📝 Track pet care tasks (walks, feeding, medications, enrichment, grooming)
- ⏰ Sort and organize tasks by time
- 🔄 Automatically recreate recurring tasks (daily/weekly)
- ⚠️ Detect scheduling conflicts
- 📊 Generate optimized daily schedules
"""
    )

st.divider()

st.subheader("Owner & Pet Information")

# Owner info
owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
available_time = st.number_input("Available time (minutes)", min_value=10, max_value=480, value=st.session_state.owner.available_time_minutes)

# Update owner if values changed
st.session_state.owner.name = owner_name
st.session_state.owner.available_time_minutes = available_time

# Pet info
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["Dog", "Cat", "Other"])
with col3:
    age = st.number_input("Age", min_value=0, max_value=30, value=3)

# Create or update pet when button is clicked
if st.button("Add/Update Pet"):
    new_pet = Pet(pet_name, species, age)
    st.session_state.owner.add_pet(new_pet)
    st.session_state.current_pet = new_pet
    st.success(f"✓ Added {pet_name} the {species}!")

# Display current pets
if st.session_state.owner.pets:
    st.write("**Current Pets:**")
    for pet in st.session_state.owner.pets:
        st.write(f"- {pet}")
        if pet == st.session_state.current_pet:
            st.caption("  👉 Currently selected for adding tasks")

st.markdown("### Tasks")
st.caption("Add tasks to the currently selected pet.")

if st.session_state.current_pet is None:
    st.warning("⚠️ Please add a pet first before adding tasks!")
else:
    col1, col2 = st.columns(2)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
        task_type = st.selectbox("Task Type", [t.value for t in TaskType])
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col2:
        priority = st.number_input("Priority (1-5)", min_value=1, max_value=5, value=5)
        scheduled_time = st.text_input("Scheduled time (HH:MM)", value="07:00", placeholder="07:00")
        frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])

    if st.button("Add Task"):
        # Convert task_type string back to TaskType enum
        task_type_enum = TaskType(task_type)
        new_task = Task(
            task_title,
            task_type_enum,
            int(duration),
            int(priority),
            frequency=frequency,
            scheduled_time=scheduled_time,
            due_date=date.today()
        )
        st.session_state.current_pet.add_task(new_task)
        st.success(f"✓ Added task '{task_title}' to {st.session_state.current_pet.name}!")

    # Display all tasks with filtering and sorting
    all_tasks = st.session_state.owner.get_all_tasks()
    if all_tasks:
        st.markdown("### 📋 Task Management")

        # Create scheduler for using its methods
        scheduler = Scheduler(st.session_state.owner)

        # Conflict detection
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            with st.expander("⚠️ SCHEDULING CONFLICTS DETECTED", expanded=True):
                for conflict in conflicts:
                    st.warning(conflict)
        else:
            st.success("✅ No scheduling conflicts detected!")

        # Filtering options
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_status = st.selectbox("Filter by Status", ["All", "Incomplete", "Completed"])
        with col2:
            pet_names = ["All"] + [pet.name for pet in st.session_state.owner.pets]
            filter_pet = st.selectbox("Filter by Pet", pet_names)
        with col3:
            task_types = ["All"] + [t.value for t in TaskType]
            filter_type = st.selectbox("Filter by Type", task_types)

        # Apply filters
        filtered_tasks = all_tasks

        if filter_status == "Incomplete":
            filtered_tasks = scheduler.filter_by_status(completed=False)
        elif filter_status == "Completed":
            filtered_tasks = scheduler.filter_by_status(completed=True)

        if filter_pet != "All":
            filtered_tasks = [t for t in filtered_tasks if t.pet and t.pet.name == filter_pet]

        if filter_type != "All":
            task_type_enum = TaskType(filter_type)
            filtered_tasks = [t for t in filtered_tasks if t.task_type == task_type_enum]

        # Sort by time
        sorted_tasks = scheduler.sort_by_time(filtered_tasks)

        # Display tasks in a table
        if sorted_tasks:
            task_data = []
            for task in sorted_tasks:
                pet_name = task.pet.name if task.pet else "Unknown"
                status_icon = "✓" if task.is_completed else "○"
                task_data.append({
                    "Status": status_icon,
                    "Pet": pet_name,
                    "Task": task.name,
                    "Type": task.task_type.value,
                    "Time": task.scheduled_time if task.scheduled_time else "Unscheduled",
                    "Duration": f"{task.duration_minutes}min",
                    "Priority": task.priority,
                    "Frequency": task.frequency,
                    "Due Date": task.due_date.strftime("%Y-%m-%d")
                })

            df = pd.DataFrame(task_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"Showing {len(sorted_tasks)} task(s) sorted by time")
        else:
            st.info("No tasks match the selected filters.")
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("🗓️ Generate Daily Schedule")
st.caption("Click to generate an optimized schedule based on priorities and available time.")

if st.button("🚀 Generate Optimized Schedule", type="primary"):
    if not st.session_state.owner.pets:
        st.error("❌ Please add at least one pet first!")
    elif not st.session_state.owner.get_all_tasks():
        st.error("❌ Please add at least one task first!")
    else:
        # Create scheduler and generate plan
        scheduler = Scheduler(st.session_state.owner)
        schedule = scheduler.generate_plan()

        # Display the schedule
        st.success("✅ Schedule Generated Successfully!")
        st.markdown("### 📅 Today's Optimized Schedule")

        # Display schedule details with metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Time Used", f"{schedule.get_total_duration()} min")
        with col2:
            st.metric("Available Time", f"{st.session_state.owner.available_time_minutes} min")
        with col3:
            remaining = st.session_state.owner.available_time_minutes - schedule.get_total_duration()
            st.metric("Remaining Time", f"{remaining} min")

        if schedule.tasks:
            st.markdown("#### 📋 Scheduled Tasks")

            # Display tasks in a nice table
            schedule_data = []
            for i, task in enumerate(schedule.tasks, 1):
                pet_name = task.pet.name if task.pet else "Unknown"
                status_icon = "✓" if task.is_completed else "○"
                schedule_data.append({
                    "#": i,
                    "Status": status_icon,
                    "Task": task.name,
                    "Pet": pet_name,
                    "Type": task.task_type.value,
                    "Time": task.scheduled_time if task.scheduled_time else "-",
                    "Duration": f"{task.duration_minutes} min",
                    "Priority": "⭐" * task.priority
                })

            df = pd.DataFrame(schedule_data)
            st.table(df)
        else:
            st.warning("⚠️ No tasks could be scheduled.")

        # Display reasoning in an info box
        st.markdown("#### 🤔 Scheduling Reasoning")
        st.info(schedule.get_reasoning())

        # Display conflicts report
        st.markdown("#### ⚠️ Conflict Check")
        conflict_report = scheduler.get_conflicts_report()
        if "No scheduling conflicts" in conflict_report:
            st.success(conflict_report)
        else:
            st.warning(conflict_report)
