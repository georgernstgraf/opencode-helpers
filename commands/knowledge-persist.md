---
description: Persist session knowledge to docs/ai/ files
---

Review our entire conversation and update the knowledge files in
docs/ai/.
Use the knowledge-persistence skill for this.

For each file, only add what is new or changed. Do not duplicate
existing entries. Write directly to disk.

Then commit and push the updated knowledge files (its own commit with the
active issue reference; SVN: `svn ci`) — persistence is only complete once the
changes are on the trunk. Never create an empty commit, and never close/reopen
an issue here.
