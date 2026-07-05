# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked it to add a third scheduling feature beyond the basics: a "next available slot" method that suggests the next free time of day to fit a new task, and to wire it into the demo and the tests without breaking anything that already worked.

**What did the agent do?**

It edited four files:

- `pawpal_system.py`: added a `next_available_slot` method on the `Scheduler`, plus two small helpers to convert between "HH:MM" strings and minutes.
- `main.py`: added a line to the demo that prints the next free slot after 08:00.
- `tests/test_pawpal.py`: added three tests (a free schedule returns the start time, taken times get skipped, and a completed task frees its slot back up).
- `README.md`: added the feature to the Features list and the Smarter Scheduling table.

It then ran `python main.py` and the full `pytest` suite to check everything still worked.

**What did you have to verify or fix manually?**

I ran `python3 -m pytest` and `python3 main.py` myself to confirm the output instead of trusting it worked. The part I checked most closely was that the next slot actually skipped booked times and that a finished task counted as free again. That last bit was the trickiest: the method has to filter out completed tasks before checking which slots are taken, otherwise a done task would block its own time forever. After that all 20 tests passed and the demo printed 08:30 as the next free slot, which is what I expected.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | | |
| **Response summary** | | |
| **What was useful** | | |
| **Problems noticed** | | |
| **Decision** | | |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->
