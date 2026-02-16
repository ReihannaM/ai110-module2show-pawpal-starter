import streamlit as st
from pawpal_system import Pet, Owner, Task, TaskType, Scheduler, Schedule

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# Initialize Owner in session state (only once!)
if 'owner' not in st.session_state:
    st.session_state.owner = Owner("Jordan", available_time_minutes=120)

# Initialize current pet in session state
if 'current_pet' not in st.session_state:
    st.session_state.current_pet = None

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
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
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        task_type = st.selectbox("Task Type", [t.value for t in TaskType])
    with col3:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col4:
        priority = st.number_input("Priority (1-5)", min_value=1, max_value=5, value=5)

    if st.button("Add Task"):
        # Convert task_type string back to TaskType enum
        task_type_enum = TaskType(task_type)
        new_task = Task(task_title, task_type_enum, int(duration), int(priority))
        st.session_state.current_pet.add_task(new_task)
        st.success(f"✓ Added task '{task_title}' to {st.session_state.current_pet.name}!")

    # Display all tasks for all pets
    all_tasks = st.session_state.owner.get_all_tasks()
    if all_tasks:
        st.write("**All Tasks:**")
        for pet in st.session_state.owner.pets:
            pet_tasks = pet.get_tasks()
            if pet_tasks:
                st.write(f"**{pet.name}'s tasks:**")
                for task in pet_tasks:
                    st.write(f"  {task}")
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Generate Daily Schedule")
st.caption("Click to generate an optimized schedule based on priorities and available time.")

if st.button("Generate Schedule"):
    if not st.session_state.owner.pets:
        st.error("❌ Please add at least one pet first!")
    elif not st.session_state.owner.get_all_tasks():
        st.error("❌ Please add at least one task first!")
    else:
        # Create scheduler and generate plan
        scheduler = Scheduler(st.session_state.owner)
        schedule = scheduler.generate_plan()

        # Display the schedule
        st.success("✅ Schedule Generated!")
        st.markdown("### 📅 Today's Schedule")

        # Display schedule details
        st.info(f"**Total Duration:** {schedule.get_total_duration()} / {st.session_state.owner.available_time_minutes} minutes")

        if schedule.tasks:
            st.markdown("**Scheduled Tasks:**")
            for i, task in enumerate(schedule.tasks, 1):
                st.write(f"{i}. {task}")
        else:
            st.warning("No tasks could be scheduled.")

        # Display reasoning
        st.markdown("### 🤔 Scheduling Reasoning")
        st.write(schedule.get_reasoning())
