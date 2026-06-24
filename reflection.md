# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial design centered on five classes plus an enum:

- **`Owner`** — represents the busy pet owner. Holds the owner's pets, their daily
  `available_minutes` (time budget), and a `preferences` map. Responsible for
  registering pets (`add_pet`), recording preferences (`set_preference`), and
  gathering every task across all pets (`all_tasks`).
- **`Pet`** — a single animal with a `name` and `kind`, owning the list of care
  tasks that belong to it (`add_task`).
- **`Task`** — one unit of pet care (the action, its `TaskType`, estimated
  `duration`, `priority`, and `preferred_time`). Responsible for tracking its own
  completion (`mark_complete`).
- **`TaskType`** — an enum of the care categories (walk, feeding, meds, enrichment,
  grooming) so categories are fixed values instead of loose strings.
- **`Scheduler`** — the brain of the app. Given a list of tasks, a time budget, and
  preferences, it ranks tasks (`rank_tasks`), checks each against the constraints
  (`_fits_constraints`), and produces the daily plan (`build_plan`).
- **`DailyPlan`** — the output. Holds the `scheduled_tasks`, the `skipped_tasks`,
  and an `explanation`, and can describe why the plan looks the way it does
  (`explain_choices`).

The key responsibility split is data vs. behavior: `Owner`/`Pet`/`Task`/`DailyPlan`
are data records (dataclasses), while `Scheduler` carries the planning logic.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes. After reviewing my skeleton with an AI assistant, I made the following change:

- **Added a `pet_name` field to `Task`.** My original dataclasses had `Pet` hold a
  list of `Task`s, but a `Task` had no reference back to its pet. The `Scheduler`
  works from a flattened list of all tasks (`Owner.all_tasks()`), so once flattened
  there was no way to tell which pet each task belonged to. That broke the
  scenario's requirement that the plan *explain* its choices — it could say "scheduled
  a walk" but not "walk Rex," which is meaningless with more than one pet. I added a
  lightweight `pet_name` string (stamped by `Pet.add_task`) instead of a full back-
  reference to the `Pet` object, to keep the relationship simple and avoid a circular
  dependency between the two dataclasses.

The AI review also flagged two issues I chose **not** to change yet: `rank_tasks()`
has no tie-breaker, and `preferred_time` is a free-form string that can't detect
time-of-day collisions. I left these as known tradeoffs (discussed in section 2)
rather than over-engineering the first iteration.

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
