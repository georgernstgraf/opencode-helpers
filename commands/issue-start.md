---
description: Start or continue working on a task (existing or new)
---
Let's work on the task: $ARGUMENTS

- If an issue ID is provided: 
    - Fetch the issue via `gh issue view` (including comments).
    - Assess the codebase. If the functionality is already implemented, close the issue with a comment explaining why and STOP.
- If "new" is provided or no issue exists: 
    - Create a new issue based on our current context/plan and use its ID going forward.
- If we have a plan but no issue: 
    - Create the issue from the plan now.
- Resolve any ambiguities with the user.
- Once clear: Update the issue description or add a comment with the current TODO list/plan.
- Implement the changes.
- when done, do NOT commit yet! Let the user review your changes.
