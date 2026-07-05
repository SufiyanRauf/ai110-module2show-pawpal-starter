# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

PawPal+ is built around three things a user can do. First, they set up an owner and add one or more pets, entering details like the pet's name, species, and breed. Second, they add care tasks to each pet, like walks, feeding, grooming, or medication, and each task has a time of day and how often it repeats. Third, they generate and view a daily plan, where the app pulls the tasks from all the pets together, sorts them by time, and warns about any that clash at the same time. So the three core actions are adding a pet, adding tasks to a pet, and viewing the day's schedule across all of them.

- Briefly describe your initial UML design. 
My first design broke the application into four classes based on how a user would actually use it. You set up a pet and an owner, you add tasks, and then a scheduler builds the daily plan. I tried to keep the data stuff like pet, tasks seperate from the thinking part (the scheduler) so all of the logic lives in one place instead of being spread out. I used Mermaid first before writing any code so I could see clear relationships and connections between the pieces. 

- What classes did you include, and what responsibilities did you assign to each? 
I decided to use these four classes: 
1. Pet: holds the basic information about the pet like name, species, and breed, and it also keeps its own list of tasks. So a pet knows about the tasks that belong to it. 
2. Task: represents one care activity like a walk, feeding, or medication. It keeps track of the description, the time of day it happens, how often it repeats, and whether it's been done yet. It can also mark itself as complete. 
3. Owner: holds the owner's name and their list of pets. Its main job is managing the pets and giving back all the tasks across every pet in one list, so you don't have to dig into each pet yourself. 
4. Scheduler: this class does the actual work in the application. It grabs all the tasks from the owner, organizes them by skipping the ones already done and sorting the rest by time, and it can also mark a task complete or explain what is still left for the day. 

**b. Design changes**

- Did your design change during implementation? 
Yeah, it changed a good amount. My first version was built around a single pet, and I ended up reworking it so an owner could have more than one. 

- If yes, describe at least one change and why you made it. 
The biggest change was going from one pet to multiple pets, and moving where the tasks live. At first the owner held one pet and the whole task list sat on the owner. But that only worked if you had a single pet, and it didn't really make sense that the owner owned the tasks instead of the pet they belonged to. So I moved the task list onto the Pet class, and gave the Owner a list of pets. The tricky part was that the Scheduler now needed tasks from every pet, not just one place. I fixed that by adding an all_tasks method on the Owner that loops through the pets and returns everything in one list, so the Scheduler just calls that instead of reaching into each pet itself.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
The main constraint my scheduler works with is time, specifically the time of day each task is set for. It sorts everything by time so the day reads in order, and it uses time to spot conflicts when two tasks land in the same slot. It also looks at whether a task is already done, so finished tasks drop off the plan, and how often a task repeats so daily and weekly tasks come back on their own.

- How did you decide which constraints mattered most?
I focused on time because that's what actually matters when a pet owner is trying to get through the day in order. I dropped the priority and duration idea I had early on, since for this app just knowing when things happen was enough, and adding more fields would have made it more complicated without much payoff.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
My conflict detection only flags tasks that are set to the exact same time, not tasks that overlap. So if a walk is at 08:00 and feeding is at 08:15, it won't catch that even though in real life they'd overlap. It only warns when two tasks share the same "HH:MM" slot, like two things both at 08:00.

- Why is that tradeoff reasonable for this scenario?
It's reasonable because my tasks only store a start time, not how long they take, so there's no duration to compare for overlap. Checking for exact matches is simple and easy to read, and it still catches the most obvious double-booking, which is the common case for a pet owner planning their day. If I added durations later I could make the check smarter, but for now the simpler version does the job without extra complexity I don't need yet.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used AI throughout, but for different things at each stage. Early on it helped me brainstorm the classes and turn my ideas into a UML diagram. Later I used it to generate the class skeletons, write the scheduling methods, and draft tests. It was also really useful for debugging and for explaining Python I hadn't used before, like dataclasses and timedelta. The chat and inline editing were the features I leaned on most, since I could point at a specific file or method and work on just that part.

- What kinds of prompts or questions were most helpful?
The most helpful prompts were specific ones tied to a file or a method, like asking how to sort tasks in HH:MM format with a lambda, or how to detect conflicts without crashing the program. Open-ended "build the whole thing" prompts were less useful because I couldn't follow what was happening. Asking the AI to explain its own code before I saved it turned out to be one of the best habits.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
At one point the design had the Scheduler storing its own copy of the tasks and the available time, which basically duplicated what the Owner already held. I didn't accept that because it meant two sources of truth for the same data. I changed it so the Scheduler takes what it needs as inputs instead of storing it. I also cut an early version that had a whole Plan class and priority sorting, since it was more than this app needed and made the code harder to follow.

- How did you evaluate or verify what the AI suggested?
I mostly verified by running things. I ran main.py in the terminal to watch the real output, and I leaned on the pytest suite to confirm the sorting, recurrence, and conflict logic did what I expected. When a test failed I'd figure out whether the bug was in my test or in the actual logic before changing anything.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I tested the core behaviors: adding tasks to a pet, collecting tasks across all of an owner's pets, sorting by time, filtering by pet and by status, conflict detection, and recurring tasks creating the next occurrence. I also added edge cases like an owner with no pets and a pet with no tasks.

- Why were these tests important?
These are the parts that make the app actually work, so if any of them broke the schedule would come out wrong. The edge cases mattered because empty states are easy to forget and are exactly where code tends to crash.

**b. Confidence**

- How confident are you that your scheduler works correctly?
Pretty confident for the normal cases. All 17 tests pass, and I've run the demo enough times to trust the sorting, conflicts, and recurrence. I'd give it about a 4 out of 5.

- What edge cases would you test next if you had more time?
I'd test tasks that overlap in duration instead of only matching exact times, and badly formatted times like "8:00" or "25:00". I'd also want to see how it holds up with a lot of pets and tasks at once.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I'm most satisfied with how clean the final design turned out. Moving the tasks onto the Pet and letting the Owner hand back all_tasks made the Scheduler simple, and the algorithmic methods each do one clear thing. Getting all the tests to pass felt good too.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
If I did another pass I'd add durations to tasks so conflict detection could catch real overlaps, not just exact matches. I'd also show each recurring task's due date in the schedule so the recurrence is easier to see in the UI.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
The biggest thing I learned is that I have to stay the architect even when the AI can write code fast. The AI is great at producing options, but it was on me to decide what fit the design, cut what wasn't needed, and verify it actually worked. Keeping separate chat sessions for each phase helped with that. My planning chat stayed about design, my testing chat stayed about tests, and I didn't lose track in one giant messy conversation.
