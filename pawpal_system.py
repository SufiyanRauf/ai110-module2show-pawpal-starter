"""PawPal+ logic layer: core classes for planning pet care tasks."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Pet:
    """A pet being cared for."""

    name: str
    species: str
    breed: str

    def describe(self) -> str:
        """Return a readable summary of the pet."""
        ...


@dataclass
class Task:
    """A single unit of pet care work (e.g., a walk or feeding)."""

    name: str
    duration: int          # minutes
    priority: str          # "high" | "medium" | "low"
    category: str          # walk, feeding, meds, grooming, ...

    def is_high_priority(self) -> bool:
        """Return True if this task is high priority."""
        ...

    def describe(self) -> str:
        """Return a readable one-line summary of the task."""
        ...


@dataclass
class Owner:
    """The pet owner, holding the pet, the task list, and time constraints."""

    name: str
    available_minutes: int
    preferences: str = ""
    pet: Pet | None = None
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a Task to this owner's task list."""
        ...

    def time_budget(self) -> int:
        """Return how many minutes are available for care today."""
        ...


class Scheduler:
    """Turns an owner's tasks + time budget into a daily plan."""

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Return tasks ordered for planning (e.g., by priority)."""
        ...

    def filter_tasks(self, tasks: list[Task], minutes: int) -> list[Task]:
        """Return only the tasks that fit within the given minutes."""
        ...

    def generate_plan(self, owner: Owner) -> list[Task]:
        """Return the selected, ordered tasks for the owner's day."""
        ...

    def explain(self) -> str:
        """Return a human-readable explanation of the plan's choices."""
        ...
