---
description: maybe the issue is already implemented
---
We are not sure whether issue $ARGUMENTS is already implemented.

- fetch the issue via "gh issue ... --json" and read its entire content, including comments, if not already done.
- Reading the codebase, assess whether the required functionality is already implemented.

If implemented:

- close the issue with a small comment on why you consider it already implemented. Done.
  
If not implemented:

- if you detect any ambiguities in the instructions, prompt the user
- when all ambiguities are resolved, please
  - update the issue description with the new, clarified understanding.
  - comment on the issue with a TODO list or implementation plan you made.
- Now that the github issue reflects our understanding and plans: please implement!
- when done, do NOT commit yet! Let the user review your changes.
