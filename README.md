# System Design: Coordinators, Statuses, and Connections

Decide which object owns what, and build the three shapes every system in this module is made of.

**Practicing:** coordinators, owning a collection, status-driven behavior, intermediary classes, splitting a class, refusing an invalid step

- [AI Use on This Assignment](#ai-use-on-this-assignment)
- [Setup](#setup)
- [Before You Start](#before-you-start)
  - [Syntax to recognize](#syntax-to-recognize)
  - [Look these up yourself](#look-these-up-yourself)
- [From Scratch](#from-scratch)
  - [Question 1: `Rental`](#question-1-rental)
  - [Question 2: `BikeShare`](#question-2-bikeshare)
  - [Question 3: `Repair`](#question-3-repair)
  - [Question 4: `Station`](#question-4-station)
- [Modify](#modify)
  - [Question 5: `BoroBikes`](#question-5-borobikes)
  - [Question 6: `Library`](#question-6-library)
  - [Question 7: `Delivery`](#question-7-delivery)
- [Debug](#debug)
  - [Question 8: `Depot`](#question-8-depot)
  - [Question 9: `Checkout`](#question-9-checkout)
- [Submitting](#submitting)
- [Good luck!](#good-luck)

## AI Use on This Assignment

**Tutor mode, for this whole quarter.** The AI explains, questions, quizzes,
and critiques, and you write every line you submit. Quarter 1 is where you
build the habit of writing code by hand; asking an AI to write it for you
comes later, in Quarter 2, where the job becomes judging code rather than
producing it.

For this assignment that means asking it why a method that hands back its own
list lets a caller break the rule the class enforces, or having it quiz you on
which object should create a connection until you can answer with the real-
world action it mirrors. Ask it a hundred questions — that is the whole point.
What you do not do is ask it for the answer. Paste this at the start of a chat
and it will hold for the rest of the conversation:

> You are acting as a tutor. Your job is to explain what this coding question
> is asking, clarify confusing wording, and highlight the relevant concepts I
> need to know — but do not provide the full solution or code that directly
> answers the question. Instead, rephrase the problem in simpler terms,
> identify what is being tested, and suggest what steps or thought processes
> might help. Ask me guiding questions to make sure I am thinking critically.
> Do not write the final function, algorithm, or code implementation.

You own every line you submit, and you will be asked to explain it.

## Setup

Clone your repository in `development/mod-2` and then `cd` into it. Set up
your virtual environment and make a draft branch before you start.

```sh
git clone [your_repo]
cd [your_repo]
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
git checkout -b draft
```

Run `pytest` to test the entire assignment. To run one question, pass part of
its name: `pytest -k Bike`. Every push runs the tests on GitHub and reports
which ones passed in the **Actions** tab.

Push before it is finished. Your instructor grades this against the rubric,
not against the test count, so treat submitting as a checkpoint rather than a
finish line and come back to improve it.

When you are done working on this assignment, turn off your virtual
environment by running:

```sh
deactivate
```

## Before You Start

Skim this section before you read the lessons, so you know what to look for in
them. Classes, inheritance, properties, polymorphism and decorators are all
assumed here. The new material is **deciding which object owns what** before
writing any of it.

This assignment has three sections:

1. From Scratch
2. Modify
3. Debug

**The diagram work is in the short response repo, not here.** Drawing a class
diagram and defending which way a reference points are 2.8's objectives, and no
test can grade either, so they are asked there. Do that half first — the code
here is the three shapes a diagram like that is made of.

<details>
<summary><strong>Ideas to look for</strong> — the ideas behind the questions, if you want them up front</summary>

Each question depends on one or more of these ideas. Part of the work is
deciding which.

| Idea | Lesson |
| --- | --- |
| **System design** is deciding which classes exist, what each is responsible for, and how they relate — before writing code. A diagram is where that decision gets recorded. | 2.8 |
| On a class diagram, `+` marks a public attribute and `-` marks a non-public one. Every `-` should have a reason you can say in one sentence. | 2.8 |
| A reference between two classes points one way or both. Each direction makes one question easy, and pointing both ways costs you the risk of the two sides disagreeing. | 2.8 |
| A class with more than four responsibilities has more than four reasons to change. Method names carrying a prefix, like `invoice_total`, are the signal: the prefix is doing the work a class name should do. | 2.8 |
| Every system has a **coordinator** — one object that owns the collections and is the only place the rules about changing them live. The case study's is `Venue`. | 2.9 |
| A coordinator's collections are non-public, and a method that reports on one returns a **new list**. Handing back the real list hands over the ability to break the rule the class enforces. | 2.9 |
| **Status-driven behavior** means an object holds a status and each method checks it before acting, so an invalid step is refused rather than performed. | 2.9 |
| **Validate first, then change.** An exception stops a method, it does not undo what the method already did. A refusal that half-ran is worse than no refusal. | 2.9 |
| Data belonging to a pairing rather than to either side needs a class of its own — an **intermediary**, holding a reference to both plus the data of the connection. | 2.9 |
| **Creator responsibility** is deciding which object creates a connection. The entity that performs the action in the real world is usually the answer. | 2.9 |
| Two classes that each enforce half a rule will drift, because nothing makes the halves agree. One coordinator means one place to read the rule and one place to change it. | 2.9 |

</details>

### Syntax to recognize

```python
class BikeShare:                         # the coordinator
    def __init__(self):
        self._bikes = []                 # non-public: it owns these
        self._members = []

    def rentable_bikes(self):
        return [b for b in self._bikes if b.is_rentable()]   # a NEW list

    def rent(self, member, bike):
        if member not in self._members:  # every rule, in one place
            raise ValueError(...)
        if not bike.is_rentable():
            raise ValueError(...)
        bike.needs_repair = True         # change only after every check


class Repair:                            # status-driven behavior
    def __init__(self, bike):
        self.status = "reported"

    def start(self):
        if self.status != "reported":    # refuse first
            raise ValueError(...)
        self.status = "in_progress"      # then move


class Rental:                            # the intermediary
    def __init__(self, member, bike, minutes):
        self.member = member             # the objects, not their names
        self.bike = bike
        self.minutes = minutes           # data belonging to the pairing
```

### Look these up yourself

- `list(existing)` and `existing.copy()`. Both make a new list from an old one,
  and three questions need it. Read about
  [copy](https://www.w3schools.com/python/ref_list_copy.asp) on W3Schools.
- The `is` operator against `==`. One question turns on the difference. You met
  both in Mod 1; this is the assignment where it matters.

## From Scratch

Write these functions and classes in `src/from_scratch.py`.

### Question 1: `Rental`

A member rents a bike. Where does the rental's price go?

Not on the `Member` — a member has many rentals, and the price is not a fact
about the person. Not on the `Bike` either, for the same reason. The price
belongs to the **pairing** of one member and one bike at one time, which means
it needs a class of its own.

Write `Rental`, which connects one `Member` to one `Bike` and holds the data
that belongs to neither alone.

**`Bike` and `Member` are already written for you.**

`__init__` takes a member, a bike and a number of minutes, and stores all three.

| Method | Does | Returns |
| --- | --- | --- |
| `price()` | 0.25 per minute, rounded to 2 decimal places | The number |
| `involves(member)` | Whether this rental belongs to that member | `True` or `False` |
| `__repr__` | Names both sides, as `Rental(Ana, A1)` | A string |

```python
ana = Member("Ana")
rental = Rental(ana, Bike("A1", "Grand Army", False), 40)

rental.member.name               # "Ana" — reach through to the member
rental.bike.serial               # "A1"
rental.price()                   # 10.0
rental.involves(ana)             # True
rental.involves(Member("Ben"))   # False
repr(rental)                     # "Rental(Ana, A1)"
```

Store the **objects**, not their names. `self.member = member`, not
`self.member = member.name`. A rental that holds the member can answer anything
about them; one that holds a string can only answer their name.

`involves` compares identity with `is`, not names. Two different members could
share a name, and the question being asked is whether it is *this* member.

This shape has a name worth knowing: the class exists to connect two others and
to hold what belongs to the connection. Your project will need at least one.

### Question 2: `BikeShare`

Every system in this module has one object that runs it. It owns the
collections, and it is the only place that knows the rules about changing them.
In the case study that object is the `Venue`. Here it is `BikeShare`.

Write it.

**`Bike` and `Member` are already written for you.**

`__init__` takes no arguments and starts two empty lists on the instance, one of
bikes and one of members, both **non-public**.

| Method | Does | Returns |
| --- | --- | --- |
| `add_bike(bike)` | Adds a bike to the fleet | Nothing |
| `add_member(member)` | Adds a member | Nothing |
| `rentable_bikes()` | Every bike that can be rented, as a **new** list | A list of `Bike` |
| `rent(member, bike)` | Refuses unless the member is registered **and** the bike is in the fleet **and** the bike is rentable, raising `ValueError` naming which rule failed. Otherwise marks the bike as out and returns a confirmation string | A string |

```python
share = BikeShare()
ana = Member("Ana")
bike = Bike("A1", "Grand Army", False)
share.add_member(ana)
share.add_bike(bike)

share.rent(ana, bike)                    # "Ana rented A1"
share.rent(ana, bike)                    # raises ValueError — already out

share.rent(Member("Ben"), bike)          # raises ValueError — not a member
```

"Marks the bike as out" means the coordinator takes it out of circulation, so
`rentable_bikes()` no longer offers it. Decide how, and keep that decision
inside `BikeShare`.

Two things make this a coordinator rather than a bag of lists:

- **The lists are non-public and `rentable_bikes()` returns a new list.** A
  caller who edits what it hands back cannot change the fleet. A test checks
  this.
- **Every rule lives in `rent`.** Nothing outside `BikeShare` checks whether a
  member is registered, so nothing outside can forget to.

Check all three rules before changing anything, so a refused rental leaves the
system exactly as it was. A test checks that too.

### Question 3: `Repair`

A repair moves through three statuses in order: `"reported"`, then
`"in_progress"`, then `"done"`. Each step has exactly one status it may run
from, and a step out of order has to be refused rather than performed.

Write `Repair`.

**`Bike` is already written for you.**

`__init__` takes a bike and a fault description, stores both, and starts the
status at `"reported"`.

| Method | Runs from | Moves to | Refuses with |
| --- | --- | --- | --- |
| `start()` | `"reported"` | `"in_progress"` | `ValueError` |
| `finish()` | `"in_progress"` | `"done"` | `ValueError` |
| `is_open()` | any | — | `True` unless the status is `"done"` |

```python
repair = Repair(Bike("A1", "Grand Army", True), "bent wheel")
repair.status                    # "reported"

repair.finish()                  # raises ValueError — not started
repair.status                    # "reported" — unchanged

repair.start()
repair.status                    # "in_progress"
repair.is_open()                 # True

repair.finish()
repair.status                    # "done"
repair.is_open()                 # False

repair.start()                   # raises ValueError — already done
```

Three things this question is really about:

- **The statuses are named, and the names are the only legal values.** Nothing
  outside the class should be assigning to `status` at all; the methods are the
  only way it changes.
- **Each method refuses before it moves.** Check the status, raise if it is
  wrong, and only then assign. A test calls every method from every wrong
  status and checks the status did not move.
- **The error says what went wrong.** A message naming the status it needed and
  the status it found is the difference between a useful refusal and a wall.

This is the shape project requirement 6 asks for, and it is the same shape as
the case study's `Reservation`. Next assignment you will write it again with a
decorator; here, write the checks by hand so you know what the decorator is
replacing.

### Question 4: `Station`

A station owns the bikes docked at it. Other code asks a station questions; it
does not reach into the station's list.

Write `Station`.

**`Bike` is already written for you.**

`__init__` takes a name and a capacity, and starts a **non-public** empty list
of bikes.

| Method | Does | Returns |
| --- | --- | --- |
| `dock(bike)` | Adds a bike, or raises `ValueError` if the station is full | Nothing |
| `count()` | How many bikes are here | The number |
| `has_room()` | Whether another bike would fit | `True` or `False` |
| `bikes_here()` | Every bike docked here, as a **new** list | A list of `Bike` |

```python
station = Station("Grand Army", 2)
station.count()                  # 0
station.has_room()               # True

station.dock(Bike("A1", "Grand Army", False))
station.dock(Bike("A2", "Grand Army", False))
station.has_room()               # False
station.dock(Bike("A3", "Grand Army", False))   # raises ValueError

station.bikes_here().clear()     # allowed, and changes nothing
station.count()                  # 2
```

The last two lines are the question. `bikes_here()` returns a **new** list, so a
caller may do whatever it likes to the result without touching the station. A
method that returns `self._bikes` itself hands over the station's own list, and
then any caller can append past the capacity the station is supposed to enforce
— the rule is still written in `dock`, but there is now a way around it.

That is what a non-public collection is protecting against, and copying the list
on the way out is how you protect it.

## Modify

Change the code already in `src/modify.py`.

### Question 5: `BoroBikes`

`BoroBikes` does five jobs. It tracks the fleet, which is its job. It also
prices invoices, formats invoice text, decides repair priority, and writes
mechanic rotas, which are not.

The symptom is in the method names: `invoice_total`, `invoice_text`,
`repair_priority` and `rota_for` all have a prefix doing the work a class name
should be doing.

Split it. `Invoice` and `Mechanic` are waiting in `src/modify.py`.

| Class | Keeps or gains |
| --- | --- |
| `BoroBikes` | `add_bike`, `fleet_size` — the fleet, and nothing else |
| `Invoice` | `__init__(minutes)`, `total()`, `text(name)` |
| `Mechanic` | `__init__(name)`, `priority(bike)`, `rota(days)` |

```python
share = BoroBikes()
share.add_bike("A1")
share.fleet_size()               # 1

Invoice(40).total()              # 10.0
Invoice(40).text("Ana")          # "Ana owes 10.0"

mech = Mechanic("Sam")
mech.priority("A1")              # "normal"
mech.priority("BROKEN-A1")       # "urgent"
mech.rota(2)                     # "Sam works 2 days"
```

The numbers and the strings must not change. Move the logic, do not rewrite it —
read each method's body out of `BoroBikes` and put it where it belongs.

**Delete the four moved methods from `BoroBikes`.** A test checks they are gone,
and that `BoroBikes` is down to the fleet.

The question to ask of any class is how many reasons it has to change. This one
changes when pricing changes, when invoice wording changes, when repair rules
change, when rotas change, and when the fleet changes — five reasons, so five
teams can collide in one file. `BoroBikes` keeping only the fleet leaves it with
one.

### Question 6: `Library`

`Reader.borrow` reaches into a `Book` and changes it. `Book.lend_to` reaches
into a `Reader` and changes them. Each class knows about the other, each
enforces part of the rule, and neither enforces all of it — so borrowing through
`Reader` checks the loan limit while borrowing through `Book` does not.

Give the rule one home. `Library` is waiting in `src/modify.py`.

When you are done:

- `Library.lend(reader, book)` is the only way a book is borrowed. It refuses
  with `ValueError` unless the book is available **and** the reader is under
  three loans, then records the loan on both sides.
- `Reader.borrow` and `Book.lend_to` are **deleted**.
- `Reader` and `Book` keep their data and their read-only questions.

```python
library = Library()
ana = Reader("Ana")
book = Book("Dune")

library.lend(ana, book)          # "Ana borrowed Dune"
book.on_loan                     # True
ana.loan_count()                 # 1

library.lend(Reader("Ben"), book)   # raises ValueError — already out

for title in ["A", "B"]:
    library.lend(ana, Book(title))
library.lend(ana, Book("D"))     # raises ValueError — Ana has three
```

A test checks both old methods are gone, and that a refused loan left the book
available and the reader's count unchanged.

The reason to do this is not tidiness. Two classes that each enforce half a rule
will drift, because nothing makes the halves agree. One coordinator means there
is one place to read the rule and one place to change it, and a new way to
borrow cannot appear without going through it.

### Question 7: `Delivery`

A delivery goes `"packed"`, then `"collected"`, then `"delivered"`. Two of the
three transitions check the status they run from. `deliver` does not, so a
packed delivery that nobody collected can be marked delivered.

```python
job = Delivery("A1")
job.status                       # "packed"
job.deliver()                    # should refuse, and does not
job.status                       # "delivered" — the bike was never collected
```

Fix `Delivery` in `src/modify.py` so every transition refuses from the wrong
status. Follow the shape the other two already use.

```python
job = Delivery("A1")
job.deliver()                    # raises ValueError
job.status                       # "packed"

job.collect()
job.deliver()
job.status                       # "delivered"
job.collect()                    # raises ValueError — already delivered
```

Match the existing error message style, so all three read the same way.

A missing check in one transition is the most common bug in a status machine,
and the hardest to see by reading, because the two correct methods make the
third look right by association. The way to find it is to list every status and
every method and ask what each pair should do — fifteen questions for five
statuses and three methods, and the answers are your tests.

That is also the argument for the decorator in the next assignment: with
`@requires_status("collected")` on `deliver`, this bug is a missing line you can
see from across the room rather than a missing `if` inside a body.

## Debug

Fix the code in `src/debug.py`.

### Question 8: `Depot`

`Depot` enforces a capacity. `store` refuses once the depot is full, and the
rule is correct. The depot still ends up over capacity:

```python
depot = Depot("Yard", 2)
depot.store("A1")
depot.store("A2")
depot.store("A3")                # correctly raises ValueError

depot.contents().append("A3")    # no error
depot.count()                    # 3 — over a capacity of 2
```

Nothing raised, and the rule in `store` was never run. Fix `Depot` in
`src/debug.py`.

```python
depot = Depot("Yard", 2)
depot.store("A1")
depot.contents().append("A3")
depot.count()                    # 1 — the depot is unchanged
```

`contents()` returns `self._items`, which is the depot's own list. Every caller
that receives it holds the real thing, so every caller can append to it, and the
capacity check in `store` is simply not involved.

A non-public name was not enough on its own. `_items` says *do not reach for
this*, and `contents()` then hands it over anyway — the convention was followed
and the door was left open.

Return a copy. One call fixes it, and the fix is the whole idea: a method that
reports on a collection gives back an answer, not the collection.

`store` is correct. Do not change it.

### Question 9: `Checkout`

`Checkout.complete` refuses a checkout with an empty basket. It raises the right
error. It also leaves the object broken:

```python
checkout = Checkout("Ana")
checkout.status                  # "open"

try:
    checkout.complete()
except ValueError:
    pass

checkout.status                  # "complete" — on an empty basket
checkout.items                   # [] — nothing was bought
```

The caller was told the action failed. The object says it succeeded. Fix
`Checkout` in `src/debug.py`.

```python
checkout = Checkout("Ana")

try:
    checkout.complete()
except ValueError:
    pass

checkout.status                  # "open" — the refusal changed nothing
checkout.total                   # 0

checkout.add("A1", 4.00)
checkout.complete()
checkout.status                  # "complete"
checkout.total                   # 4.0
```

Read `complete` and find the order of operations. It assigns the status, then
totals the basket, then checks whether the basket was empty. By the time the
check runs, two attributes have already moved, and raising does not put them
back — an exception stops the method, it does not undo what the method did.

**Validate first, then change.** Every refusal in this module depends on that
order, and this is what it looks like when the order is wrong.

This is also the bug the next assignment's test prompt is about: a test that
only asserts `pytest.raises(ValueError)` passes against this code. Proving a
refusal happened is not the same as proving it changed nothing.

## Submitting

```sh
git add -A
git commit -m "your message"
git push
```

Pushing runs the tests on GitHub. Check the **Actions** tab to see which
passed, then open a pull request to your instructor for feedback.

## Good luck!

Every system you build from here is made of classes, so this is the
assignment the rest of the module stands on. You got this!
