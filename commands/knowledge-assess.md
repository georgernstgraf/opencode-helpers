---
description: Assessment of knowledge tests
---
# Task: Assess Student Submissions

In this directory, you will find the submissions which students have handed
in. The "knowledge-" files contain the questions and their respective
solutions.

## Please create 3 german markdown files:

- GRADINGS.md with a comprehensive table showing the evaluations of each student (ordered alphabetically, by student, not by grade) in the Austrian grading system.
- INDIVIDUAL.md with detailed assessements of each students submissions.
- CLASS.md with the most common errors of the class and recommendations for the teacher in order to address them subsequently

## JSON for bulk email

Also create an `EMAIL.json` file which will be used to send out personalized
emails. To get the email addresses, use the sqlite3 database "vacuum.db", it
has a "users" table:

```sql
sqlite> .schema users
CREATE TABLE IF NOT EXISTS "users" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "email" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "klasse" TEXT,
    "updatedat" DATETIME NOT NULL
);
```

EMAIL.json shall be a .json array containing object with 3 fields each:

- mailto: recipient email address
- subject: Ergebnis der Wissensüberprüfung am <isodate>
- body: <YOUR INDIVIDUAL ASSESSMENT>


