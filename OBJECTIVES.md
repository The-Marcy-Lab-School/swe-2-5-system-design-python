# Objective map — assignment 2.5

**Instructor facing.** This file is for auditing the assignment against the
scope and sequence. It is not written for fellows.

Covers **2.8 System Design and UML Diagrams** and **2.9 System Design
Strategies**.

| | Name |
| --- | --- |
| Code | `swe-2-5-system-design-python` |
| Short response | `swe-sr-2-5-system-design-python` |

## 2.8 has no code-able objectives

Four of 2.8's five objectives are *draw a diagram* or *defend a design*. Only
"judge whether a class carrying too many responsibilities should be split" can
be a code question, and it is question 5. So four-fifths of 2.8 is in the short
response repo, which is four prompts rather than the usual three.

That makes this the first assignment in the module where the short response half
is the larger one, and it includes a drawing task, which nothing in Mod 1 or
Mod 2 has asked for before. The prompt accepts ASCII or a photo of paper.

2.9 carries the code: a coordinator, status-driven behavior, and an intermediary
class. Those are the three shapes the project's own system is made of, which
makes this the last code practice before the project.

## Objective map

All eleven objectives are covered.

| Objective | Covered by |
| --- | --- |
| 2.8 Create · D1 — a class diagram with responsibilities and relationships | SR 1 |
| 2.8 Apply · D1 — mark attributes `+` or `-`, one reason per `-` | SR 1 |
| 2.8 Evaluate · D1 — one-way or bidirectional, defended | SR 2 |
| 2.8 Create · D1 — a diagram from a spoken description | SR 1 |
| 2.8 Evaluate · R1 — split a class, name the replacements | Q5 `BoroBikes` |
| 2.9 Analyze · R5, R6 — the coordinator, its collections, its rules | Q2 `BikeShare`, Q6 `Library` |
| 2.9 Create · R6 — status-driven behavior and what each step refuses | Q3 `Repair`, Q7 `Delivery`, Q9 `Checkout` |
| 2.9 Create · R6 — an intermediary holding both references plus its own data | Q1 `Rental` |
| 2.9 Evaluate · D1 — which object creates the connection | SR 3 |
| 2.9 Evaluate · R6 — a coordinator or direct relationships, and one cost | Q6, SR 3 |
| 2.9 Testing · R9 — a refusal left the status and every collection unchanged | Q9, SR 4 |

45 tests. All 45 pass against the reference solutions, 38 fail against the
stubs, 7 are regression guards.

## Question 9 is the one not to cut

`Checkout.complete` assigns the status, totals the basket, and **then** checks
whether the basket was empty. It raises the correct error and leaves the object
claiming it succeeded.

That is what makes "validate first, then change" mean something, and it is
exactly the bug SR 4 asks them to write a test for — a test asserting only
`pytest.raises(ValueError)` passes against it. The code question and the short
response prompt are deliberately the same bug from two sides.

## Open question raised in the pull request

The week. This assignment lands between 2.9 and the project, so a fellow
practices coordinators in one repo while designing their own in another. If that
is too much, the honest cut is questions 1 to 4 and dropping the Modify section,
which is the part that repeats what From Scratch already taught.
