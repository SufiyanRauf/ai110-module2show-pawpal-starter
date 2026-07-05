from pawpal_system import Owner, Pet, Task, Scheduler


def test_task_starts_incomplete():
    task = Task("Walk", "08:00", "daily")
    assert task.completed is False


def test_mark_complete():
    task = Task("Walk", "08:00", "daily")
    task.mark_complete()
    assert task.completed is True


def test_pet_add_task():
    pet = Pet("Biscuit", "dog", "Golden Retriever")
    before = len(pet.tasks)
    pet.add_task(Task("Walk", "08:00", "daily"))
    assert len(pet.tasks) == before + 1


def test_owner_collects_tasks_from_all_pets():
    owner = Owner("Sam")
    dog = Pet("Biscuit", "dog", "Golden Retriever")
    cat = Pet("Miso", "cat", "Tabby")
    owner.add_pet(dog)
    owner.add_pet(cat)
    dog.add_task(Task("Walk", "08:00", "daily"))
    cat.add_task(Task("Feed", "09:00", "daily"))

    assert len(owner.all_tasks()) == 2


def test_daily_plan_sorted_by_time():
    owner = Owner("Sam")
    pet = Pet("Biscuit", "dog", "Golden Retriever")
    owner.add_pet(pet)
    pet.add_task(Task("Dinner", "18:00", "daily"))
    pet.add_task(Task("Walk", "08:00", "daily"))

    plan = Scheduler().daily_plan(owner)
    times = [t.time for t in plan]
    assert times == ["08:00", "18:00"]


def test_daily_plan_skips_completed():
    owner = Owner("Sam")
    pet = Pet("Biscuit", "dog", "Golden Retriever")
    owner.add_pet(pet)
    done = Task("Walk", "08:00", "daily", completed=True)
    pet.add_task(done)
    pet.add_task(Task("Dinner", "18:00", "daily"))

    plan = Scheduler().daily_plan(owner)
    assert done not in plan
    assert len(plan) == 1
