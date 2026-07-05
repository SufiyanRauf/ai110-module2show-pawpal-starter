# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Pawpal+ is built around three things that a user can do. The first item is that they can set up an owner and pet profile by entering owner and pet details like the name, pet type, and how much time allocated per day. The second item is that they can add and edit tasks related to pet care like grooming, walks, feeding, and medications with each having a priority and duration. The third item is that users can generate and view a daily plan, as the application can rrange the tasks into a schedule that fits within available time and prioritizes the most import task. In summary, three core actions a user should be able to perform are adding a pet, scheduling tasks like walking or feeding, and generating a schedule that allows them to view the tasks of a specific day.

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
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
