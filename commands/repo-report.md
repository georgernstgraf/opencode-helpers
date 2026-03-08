---
name: repo-report
description: Generate a repository activity report using the Repo-Report skill; optionally limit to last $1 weeks via argument
skill: repo-report
---
# /repo-report Command

This command runs the `repo-report` skill to analyze the current Git repository and produce a `report.md` file with
- Topics and content themes from commit messages
- Commit frequency per week
- Gaps longer than one week with no commits

The report is written to the repository root and is not committed.
