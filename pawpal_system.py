"""PawPal+ logic layer: core classes for planning pet care tasks."""

from __future__ import annotations

from dataclasses import dataclass, field

# Lower number = higher priority. Used to sort tasks when planning the day.
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


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

    def priority_rank(self) -> int:
        """Return a sortable rank for this task's priority (lower = sooner)."""
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


@dataclass
class Plan:
    """The result of scheduling: what made the cut, what didn't, and why."""

    scheduled: list[Task] = field(default_factory=list)
    skipped: list[Task] = field(default_factory=list)
    reason: str = ""

    def total_duration(self) -> int:
        """Return the total minutes of all scheduled tasks."""
        ...

    def summary(self) -> str:
        """Return a short one-line overview of the plan."""
        ...

    def to_display(self) -> str:
        """Return the full plan formatted for display in the UI."""
        ...


class Scheduler:
    """Turns an owner's tasks + time budget into a daily plan."""

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Return tasks ordered for planning (by priority, then duration)."""
        ...

    def filter_tasks(self, tasks: list[Task], minutes: int) -> list[Task]:
        """Return only the tasks that fit within the given minutes."""
        ...

    def generate_plan(self, owner: Owner) -> Plan:
        """Build and return a Plan from the owner's tasks and time budget."""
        ...

    def explain(self, plan: Plan) -> str:
        """Return a human-readable explanation of the plan's choices."""
        ...
