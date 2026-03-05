---
description: create knowledge_<isodate>.md klasse wochen
---
# Task: create a mini-exam

This is a teacher's repo providing documents and learning
materials to students at a technical college in vienna.

class is $1
weeks is $2

If there is no folder "$1", STOP. The user made a typo.

please create a german `knowledge_<class>_<isodate-today>.md` file within the folder `<class>` as follows:

- analyze all commits from the last $2 weeks which changed files in folder $1, using git.
- those commits are often very minimalistic. Assume the teacher explained a lot around the content of those commits during the lectures in class.
- make ~12 multiple choice questions with 1-4 true answers each, referring to the topics that were covered. Each of these questions shall have the weight of 4 points.
- also create ~3 free-form questions where the student has to answer with free text. Each of these questions shall have the weight of 10 points.
- do not put the solutions into this file, but rather:
- also create a german `knowledge_<class>_<isodate-today>_solutions.md` with the teachers solutions, the pattern `**/*_solutions.md`
should be git-ignored.
- DO NOT COMMIT
