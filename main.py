# quick script to try out the pawpal classes in the terminal
from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner("Sam")

biscuit = Pet("Biscuit", "dog", "Golden Retriever")
miso = Pet("Miso", "cat", "Tabby")
owner.add_pet(biscuit)
owner.add_pet(miso)

# added out of order on purpose so I can see the sorting actually work
biscuit.add_task(Task("Dinner", "18:00", "daily"))
biscuit.add_task(Task("Morning walk", "08:00", "daily"))
miso.add_task(Task("Clean litter box", "09:30", "daily"))
miso.add_task(Task("Flea meds", "08:00", "weekly"))  # same time as the walk -> conflict

scheduler = Scheduler()

print("Today's Schedule for " + owner.name)
print("=" * 40)
for task in scheduler.daily_plan(owner):
    print(task.describe())

print("\nJust Biscuit's tasks:")
biscuit_tasks = scheduler.filter_by_pet(owner, "Biscuit")
for task in scheduler.sort_by_time(biscuit_tasks):
    print("  " + task.describe())

print("\nConflicts:")
conflicts = scheduler.find_conflicts(owner)
if conflicts:
    for warning in conflicts:
        print("  " + warning)
else:
    print("  none")

print("\nMarking Biscuit's morning walk done (it's daily, so it should come back):")
walk = next(t for t in biscuit.tasks if t.description == "Morning walk")
upcoming = scheduler.complete_task(biscuit, walk)
print("  next walk due:", upcoming.due_date)

print("\nCompleted tasks so far:")
for task in scheduler.filter_by_status(owner.all_tasks(), completed=True):
    print("  " + task.describe())
