# PawPal+ (Module 2 Project)

**PawPal+** is a Streamlit app that helps a pet owner plan and organize care tasks across all of their pets.

## Features

- Add an owner and multiple pets, each with their own list of care tasks
- Give each task a time of day and how often it repeats (daily or weekly)
- See the day's tasks sorted into chronological order across all pets
- Filter tasks by pet or by whether they're done
- Get a warning when two tasks are booked at the same time
- Recurring tasks reschedule themselves: finishing a daily task adds tomorrow's, weekly adds next week's
- Data stays put while you use the app (Streamlit session state)

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Running `python main.py` builds a sample owner with two pets and shows the sorting, filtering, conflict detection, and recurring-task logic in the terminal:

```
Today's Schedule for Sam
========================================
08:00 - Morning walk (daily) [todo]
08:00 - Flea meds (weekly) [todo]
09:30 - Clean litter box (daily) [todo]
18:00 - Dinner (daily) [todo]

Just Biscuit's tasks:
  08:00 - Morning walk (daily) [todo]
  18:00 - Dinner (daily) [todo]

Conflicts:
  Conflict at 08:00: Morning walk (Biscuit), Flea meds (Miso)

Marking Biscuit's morning walk done (it's daily, so it should come back):
  next walk due: 2026-07-06

Completed tasks so far:
  08:00 - Morning walk (daily) [done]
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
pytest --cov
```

Note: on my Mac `python` isn't installed, only `python3`, so I run `python3 -m pytest` instead.

The tests in `tests/test_pawpal.py` cover the core behavior:

- adding tasks to a pet and collecting them across all of an owner's pets
- sorting tasks into chronological order
- filtering by pet and by completion status
- recurring tasks (a completed daily task comes back for the next day, weekly for the next week)
- conflict detection when two tasks share the same time slot
- edge cases like an owner with no pets or a pet with no tasks

Sample test output:

```
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/sufiyanrauf/Desktop/ai110-module2show-pawpal-starter
collected 17 items

tests/test_pawpal.py .................                                   [100%]

============================== 17 passed in 0.02s ==============================
```

**Confidence level:** ⭐⭐⭐⭐ (4/5). The happy paths and the main edge cases all pass, so I'm fairly confident the core logic works. I held back one star because I haven't tested things like overlapping durations or badly formatted times yet.

## 📐 Smarter Scheduling

These are the scheduling features I added, and the method that handles each one. They all live in the `Scheduler` class (plus `Task` for the recurring logic) in `pawpal_system.py`.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts tasks by their "HH:MM" time using `sorted()` with a lambda key. |
| Filtering | `Scheduler.filter_by_pet()`, `Scheduler.filter_by_status()` | Pull tasks for one pet, or only the done / not-done ones. |
| Conflict handling | `Scheduler.find_conflicts()` | Groups pending tasks by time slot and returns a warning string for any slot with more than one task. Checks exact time matches only. |
| Recurring tasks | `Task.next_occurrence()`, `Scheduler.complete_task()` | When a daily/weekly task is completed, a new copy is added with `due_date` moved ahead using `timedelta` (daily = +1 day, weekly = +7). |

## 📸 Demo Walkthrough

PawPal+ runs as a Streamlit web app. Start it with `streamlit run app.py` (or `python3 -m streamlit run app.py`).

**What you can do in the UI:**

- Set the owner's name.
- Add one or more pets (name, species, breed). Empty or duplicate names are blocked with a warning.
- Add tasks to a pet: a description, a time in HH:MM, and how often it repeats.
- See "Today's schedule" as a sorted table, with warnings above it for any time conflicts.

**Example workflow:**

1. Open the app and set the owner name (for example, "Jordan").
2. Add a pet, like "Biscuit" the dog.
3. Give Biscuit a couple of tasks: a "Morning walk" at 08:00 and "Dinner" at 18:00.
4. Add a second pet, "Miso" the cat, and give it "Flea meds" at 08:00.
5. Scroll to "Today's schedule" to see both pets' tasks sorted together by time.

**Scheduler behaviors you'll notice:**

- The schedule table is sorted by time even though tasks were added out of order and belong to different pets (`Scheduler.daily_plan` / `sort_by_time`).
- Since Biscuit's walk and Miso's meds are both at 08:00, a warning appears: "Conflict at 08:00: ..." (`Scheduler.find_conflicts`).
- Marking a daily or weekly task complete schedules its next occurrence automatically (`Scheduler.complete_task`).

**Sample CLI output** (from `python main.py`):

```
Today's Schedule for Sam
========================================
08:00 - Morning walk (daily) [todo]
08:00 - Flea meds (weekly) [todo]
09:30 - Clean litter box (daily) [todo]
18:00 - Dinner (daily) [todo]

Just Biscuit's tasks:
  08:00 - Morning walk (daily) [todo]
  18:00 - Dinner (daily) [todo]

Conflicts:
  Conflict at 08:00: Morning walk (Biscuit), Flea meds (Miso)

Marking Biscuit's morning walk done (it's daily, so it should come back):
  next walk due: 2026-07-06

Completed tasks so far:
  08:00 - Morning walk (daily) [done]
```
