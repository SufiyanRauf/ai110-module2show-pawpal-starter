from datetime import date

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


def test_sort_by_time():
    tasks = [Task("Dinner", "18:00", "daily"), Task("Walk", "08:00", "daily")]
    ordered = Scheduler().sort_by_time(tasks)
    assert [t.time for t in ordered] == ["08:00", "18:00"]


def test_filter_by_status():
    done = Task("Walk", "08:00", "daily", completed=True)
    todo = Task("Dinner", "18:00", "daily")
    sched = Scheduler()
    assert sched.filter_by_status([done, todo], completed=True) == [done]
    assert sched.filter_by_status([done, todo], completed=False) == [todo]


def test_filter_by_pet():
    owner = Owner("Sam")
    dog = Pet("Biscuit", "dog", "Golden Retriever")
    cat = Pet("Miso", "cat", "Tabby")
    owner.add_pet(dog)
    owner.add_pet(cat)
    dog.add_task(Task("Walk", "08:00", "daily"))
    cat.add_task(Task("Feed", "09:00", "daily"))

    tasks = Scheduler().filter_by_pet(owner, "Biscuit")
    assert len(tasks) == 1
    assert tasks[0].description == "Walk"


def test_find_conflicts_flags_same_time():
    owner = Owner("Sam")
    dog = Pet("Biscuit", "dog", "Golden Retriever")
    cat = Pet("Miso", "cat", "Tabby")
    owner.add_pet(dog)
    owner.add_pet(cat)
    dog.add_task(Task("Walk", "08:00", "daily"))
    cat.add_task(Task("Feed", "08:00", "daily"))

    conflicts = Scheduler().find_conflicts(owner)
    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]


def test_no_conflict_when_times_differ():
    owner = Owner("Sam")
    pet = Pet("Biscuit", "dog", "Golden Retriever")
    owner.add_pet(pet)
    pet.add_task(Task("Walk", "08:00", "daily"))
    pet.add_task(Task("Dinner", "18:00", "daily"))

    assert Scheduler().find_conflicts(owner) == []


def test_daily_task_recurs_next_day():
    pet = Pet("Biscuit", "dog", "Golden Retriever")
    walk = Task("Walk", "08:00", "daily", due_date=date(2026, 1, 1))
    pet.add_task(walk)

    upcoming = Scheduler().complete_task(pet, walk)
    assert walk.completed is True
    assert upcoming.due_date == date(2026, 1, 2)
    assert len(pet.tasks) == 2


def test_weekly_task_recurs_a_week_later():
    pet = Pet("Miso", "cat", "Tabby")
    meds = Task("Flea meds", "08:00", "weekly", due_date=date(2026, 1, 1))
    pet.add_task(meds)

    upcoming = Scheduler().complete_task(pet, meds)
    assert upcoming.due_date == date(2026, 1, 8)


def test_one_off_task_does_not_recur():
    pet = Pet("Miso", "cat", "Tabby")
    bath = Task("Bath", "10:00", "once")
    pet.add_task(bath)

    upcoming = Scheduler().complete_task(pet, bath)
    assert upcoming is None
    assert len(pet.tasks) == 1
