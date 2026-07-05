# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

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

Sample test output:

```
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/sufiyanrauf/Desktop/ai110-module2show-pawpal-starter
collected 14 items

tests/test_pawpal.py ..............                                      [100%]

============================== 14 passed in 0.01s ==============================
```

## 📐 Smarter Scheduling

These are the scheduling features I added, and the method that handles each one. They all live in the `Scheduler` class (plus `Task` for the recurring logic) in `pawpal_system.py`.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts tasks by their "HH:MM" time using `sorted()` with a lambda key. |
| Filtering | `Scheduler.filter_by_pet()`, `Scheduler.filter_by_status()` | Pull tasks for one pet, or only the done / not-done ones. |
| Conflict handling | `Scheduler.find_conflicts()` | Groups pending tasks by time slot and returns a warning string for any slot with more than one task. Checks exact time matches only. |
| Recurring tasks | `Task.next_occurrence()`, `Scheduler.complete_task()` | When a daily/weekly task is completed, a new copy is added with `due_date` moved ahead using `timedelta` (daily = +1 day, weekly = +7). |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
