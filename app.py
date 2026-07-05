import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("Plan the day's care tasks across all your pets.")

# Streamlit reruns this whole file on every click, so a fresh Owner would wipe
# the data each time. Keep one Owner in session_state and reuse it instead.
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

owner = st.session_state.owner
owner.name = st.text_input("Owner name", value=owner.name)

st.divider()

st.subheader("Add a pet")
with st.form("add_pet", clear_on_submit=True):
    name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    breed = st.text_input("Breed", value="")
    if st.form_submit_button("Add pet"):
        existing = [p.name for p in owner.pets]
        if not name.strip():
            st.warning("Please enter a pet name.")
        elif name in existing:
            st.warning(f"You already have a pet named {name}.")
        else:
            owner.add_pet(Pet(name, species, breed))
            st.success(f"Added {name}")

if owner.pets:
    st.write("Your pets: " + ", ".join(p.name for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Add a task")
if owner.pets:
    with st.form("add_task", clear_on_submit=True):
        pet_name = st.selectbox("For which pet?", [p.name for p in owner.pets])
        description = st.text_input("Task", value="Morning walk")
        time = st.text_input("Time (HH:MM)", value="08:00")
        frequency = st.selectbox("Frequency", ["daily", "weekly"])
        if st.form_submit_button("Add task"):
            pet = next(p for p in owner.pets if p.name == pet_name)
            pet.add_task(Task(description, time, frequency))
            st.success(f"Added {description} for {pet_name}")
else:
    st.caption("Add a pet first, then you can give it tasks.")

st.divider()

st.subheader("Today's schedule")
plan = Scheduler().daily_plan(owner)
if plan:
    for task in plan:
        st.write(task.describe())
else:
    st.info("Nothing scheduled yet. Add some tasks to see the plan.")
