"""PawPal+ logic layer: core classes for planning pet care tasks."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta

# how many days to jump ahead when a recurring task is completed
REPEAT_DAYS = {"daily": 1, "weekly": 7}

# lower number sorts first, so High priority comes before Low
PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}


def _to_minutes(hhmm):
    """Turn an "HH:MM" string into minutes since midnight."""
    hours, minutes = hhmm.split(":")
    return int(hours) * 60 + int(minutes)


def _to_hhmm(total_minutes):
    """Turn minutes since midnight back into an "HH:MM" string."""
    return f"{total_minutes // 60:02d}:{total_minutes % 60:02d}"


@dataclass
class Task:
    """A single pet care activity, e.g. a walk or a dose of medication."""

    description: str
    time: str                 # time of day, e.g. "08:00"
    frequency: str            # e.g. "daily", "weekly"
    priority: str = "Medium"  # "Low", "Medium", or "High"
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def next_occurrence(self) -> Task | None:
        """Return the next copy of this task, or None if it does not repeat."""
        step = REPEAT_DAYS.get(self.frequency)
        if step is None:
            return None
        return Task(self.description, self.time, self.frequency,
                    priority=self.priority,
                    due_date=self.due_date + timedelta(days=step))

    def describe(self) -> str:
        """Return a readable one-line summary of the task."""
        status = "done" if self.completed else "todo"
        return f"{self.time} - {self.description} ({self.frequency}) [{self.priority}] [{status}]"


@dataclass
class Pet:
    """A pet, including its own list of care tasks."""

    name: str
    species: str
    breed: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet."""
        self.tasks.append(task)

    def describe(self) -> str:
        """Return a readable summary of the pet."""
        return f"{self.name} the {self.breed} ({self.species})"


@dataclass
class Owner:
    """A pet owner who manages one or more pets and all their tasks."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def all_tasks(self) -> list[Task]:
        """Return every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Retrieves, organizes, and manages tasks across all of an owner's pets."""

    def get_tasks(self, owner: Owner) -> list[Task]:
        """Retrieve every task the owner has, across all pets."""
        return owner.all_tasks()

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return the tasks ordered by their HH:MM time."""
        return sorted(tasks, key=lambda t: t.time)

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Return the tasks ordered by priority first (High to Low), then by time."""
        return sorted(tasks, key=lambda t: (PRIORITY_ORDER.get(t.priority, 1), t.time))

    def filter_by_status(self, tasks: list[Task], completed: bool) -> list[Task]:
        """Return only the tasks that match the given completed flag."""
        return [t for t in tasks if t.completed == completed]

    def filter_by_pet(self, owner: Owner, pet_name: str) -> list[Task]:
        """Return the tasks belonging to the pet with this name."""
        tasks = []
        for pet in owner.pets:
            if pet.name == pet_name:
                tasks.extend(pet.tasks)
        return tasks

    def daily_plan(self, owner: Owner) -> list[Task]:
        """Return the owner's not-yet-done tasks, ordered by priority then time."""
        pending = self.filter_by_status(owner.all_tasks(), completed=False)
        return self.sort_by_priority(pending)

    def complete_task(self, pet: Pet, task: Task) -> Task | None:
        """Mark a task done, and if it repeats, add its next occurrence to the pet."""
        task.mark_complete()
        upcoming = task.next_occurrence()
        if upcoming is not None:
            pet.add_task(upcoming)
        return upcoming

    def find_conflicts(self, owner: Owner) -> list[str]:
        """Return a warning for each time slot that has more than one pending task."""
        by_time = {}
        for pet in owner.pets:
            for task in pet.tasks:
                if task.completed:
                    continue
                by_time.setdefault(task.time, []).append((pet, task))

        warnings = []
        for slot, items in sorted(by_time.items()):
            if len(items) > 1:
                names = ", ".join(f"{t.description} ({p.name})" for p, t in items)
                warnings.append(f"Conflict at {slot}: {names}")
        return warnings

    def next_available_slot(self, owner: Owner, after: str = "08:00",
                            step_minutes: int = 30) -> str | None:
        """Suggest the next open time slot at or after `after`, or None if the day is full."""
        taken = {t.time for t in self.filter_by_status(owner.all_tasks(), completed=False)}
        minutes = _to_minutes(after)
        while minutes < 24 * 60:
            slot = _to_hhmm(minutes)
            if slot not in taken:
                return slot
            minutes += step_minutes
        return None

    def explain(self, owner: Owner) -> str:
        """Return a short human-readable summary of today's plan."""
        plan = self.daily_plan(owner)
        if not plan:
            return "No tasks left for today. All caught up!"
        lines = [t.describe() for t in plan]
        return f"{len(plan)} task(s) to do today:\n" + "\n".join(lines)
