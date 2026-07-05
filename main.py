# quick script to try out the pawpal classes in the terminal
from pawpal_system import Owner, Pet, Task

owner = Owner("Sam")

biscuit = Pet("Biscuit", "dog", "Golden Retriever")
miso = Pet("Miso", "cat", "Tabby")
owner.add_pet(biscuit)
owner.add_pet(miso)

biscuit.add_task(Task("Morning walk", "08:00", "daily"))
biscuit.add_task(Task("Dinner", "18:00", "daily"))
miso.add_task(Task("Clean litter box", "09:30", "daily"))
miso.add_task(Task("Flea meds", "07:00", "weekly"))

# pair each task with its pet so the schedule can show whose task it is
schedule = []
for pet in owner.pets:
    for task in pet.tasks:
        schedule.append((pet, task))

schedule.sort(key=lambda pair: pair[1].time)

print("Today's Schedule for " + owner.name)
print("=" * 40)
for pet, task in schedule:
    box = "[x]" if task.completed else "[ ]"
    print(f"{box} {task.time}  {task.description.ljust(18)} ({pet.name}, {task.frequency})")
