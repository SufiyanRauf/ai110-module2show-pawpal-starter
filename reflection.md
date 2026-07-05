# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Pawpal+ is built around three things that a user can do. The first item is that they can set up an owner and pet profile by entering owner and pet details like the name, pet type, and how much time allocated per day. The second item is that they can add and edit tasks related to pet care like grooming, walks, feeding, and medications with each having a priority and duration. The third item is that users can generate and view a daily plan, as the application can rrange the tasks into a schedule that fits within available time and prioritizes the most import task. In summary, three core actions a user should be able to perform are adding a pet, scheduling tasks like walking or feeding, and generating a schedule that allows them to view the tasks of a specific day.

- Briefly describe your initial UML design. 
My first design broke the application into four classes based on how a user would actually use it. You set up a pet and an owner, you add tasks, and then a scheduler builds the daily plan. I tried to keep the data stuff like pet, tasks seperate from the thinking part (the scheduler) so all of the logic lives in one place instead of being spread out. I utilized the Mermaid technique first before code was written so I could see clear relationships and connections between the pieces. 

- What classes did you include, and what responsibilities did you assign to each? 
I decided to use these four classes: 
1. Pet: holds the basic information about the pet like name, species, and breed. The main purpose is to just store data. 
2. Task: represents one car task like a walk or feeding or medication. It keeps track of the name, how long the task takes, the priority, and the category. It is responsible for letting you know if it is high priority. 
3. Owner: contains the owner's name, how much time they have that day, preferences, their pet, and the list of tasks associated with pet. Its main responsibility is to mantain the task list and report how many minutes are free. 
4.Scheduler: this class does the actual work in the application. It takes the owner's tasks and time and figures out the plan by sorting tasks by priority. The tasks that don't fit in the time left are dropped, and the scheduler explains its reasoning on why it picked the schedule that it did. 

**b. Design changes**

- Did your design change during implementation? 
Yeah, it changed a few times. My first version was more complicated than it needed to be, and I ended up cutting stuff and then adding one thing back once I realized the scheduler couldn't actually do what I wanted. 

- If yes, describe at least one change and why you made it. 
The biggest change was adding a Plan class. Aft first, my scheduler just returned a list of tasks, but one of the requirements is to explain why it picked the plan it did. When I looked at it again, the explain method had no way to know what got scheduled or what got skipped, since all it got back was a plain list. So I made a Plan object that holds the scheduled tasks, the skipped tasks, and a reason string. Now generate_plan returns that instead of a bare list, and explain can actually use it.

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
