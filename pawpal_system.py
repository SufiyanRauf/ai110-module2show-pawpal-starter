"""PawPal+ logic layer: core classes for planning pet care tasks."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Task:
    """A single pet care activity, e.g. a walk or a dose of medication."""

    description: str
    time: str                 # time of day, e.g. "08:00"
    frequency: str            # e.g. "daily", "weekly"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def describe(self) -> str:
        """Return a readable one-line summary of the task."""
        status = "done" if self.completed else "todo"
        return f"{self.time} - {self.description} ({self.frequency}) [{status}]"


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

    def daily_plan(self, owner: Owner) -> list[Task]:
        """Return the owner's not-yet-done tasks, ordered by time of day."""
        pending = [t for t in owner.all_tasks() if not t.completed]
        return sorted(pending, key=lambda t: t.time)

    def tasks_for_pet(self, pet: Pet) -> list[Task]:
        """Return one pet's tasks, ordered by time of day."""
        return sorted(pet.tasks, key=lambda t: t.time)

    def mark_complete(self, task: Task) -> None:
        """Mark a task as done."""
        task.mark_complete()

    def explain(self, owner: Owner) -> str:
        """Return a short human-readable summary of today's plan."""
        plan = self.daily_plan(owner)
        if not plan:
            return "No tasks left for today. All caught up!"
        lines = [t.describe() for t in plan]
        return f"{len(plan)} task(s) to do today:\n" + "\n".join(lines)
