import ast
import inspect
import textwrap


def attributes_set_on(instance):
    """The attribute names stored on this instance rather than on its class.

    An attribute written in the class body is shared by every instance, so it
    does not appear here. One assigned to self in __init__ does.
    """
    return set(vars(instance))


def assigns_in_class_body(cls):
    """The names assigned directly in a class body, read with the ast module.

    The source is parsed rather than searched as text, so a name mentioned in a
    comment or a docstring never counts.
    """
    source = textwrap.dedent(inspect.getsource(cls))
    body = ast.parse(source).body[0].body
    names = set()
    for node in body:
        if isinstance(node, ast.Assign):
            names.update(t.id for t in node.targets if isinstance(t, ast.Name))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names.add(node.target.id)
    return names

def code_of(func):
    """A function's source with its comments and docstring removed.

    A test that bans a substring has to look at code only. Reading raw source
    fails a fellow who mentions the banned thing in a comment -- "no isinstance
    here" would fail a check for "isinstance" -- which is a correct answer
    rejected for its prose.
    """
    source = textwrap.dedent(inspect.getsource(func))
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
            body = node.body
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                node.body = body[1:] or [ast.Pass()]
    return ast.unparse(ast.fix_missing_locations(tree))

def as_written(module, name, cls=None):
    """One function's body as it appears in the file, with decorators ignored.

    Reading a decorated function at runtime gives you the wrapper, so its own
    body is out of reach. Parsing the file instead shows what the fellow wrote,
    and works whatever shape their decorator took -- a closure, a class with
    __call__, or functools.wraps on top of either.
    """
    tree = ast.parse(inspect.getsource(module))
    scope = tree.body
    if cls is not None:
        scope = next(n.body for n in tree.body
                     if isinstance(n, ast.ClassDef) and n.name == cls)
    found = next((n for n in scope
                  if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                  and n.name == name), None)
    assert found is not None, f"Keep a function named {name}."
    return "\n".join(ast.unparse(stmt) for stmt in found.body)


from from_scratch import Bike, BikeShare, Member, Rental, Repair, Station


TEST_SUITE_NAME = "From Scratch Tests"


def test_rental_holds_both_objects():
    """Rental - the member and the bike are stored as objects, not names"""
    ana = Member("Ana")
    bike = Bike("A1", "Grand Army", False)
    rental = Rental(ana, bike, 40)

    assert rental.member is ana, "Store the Member object itself."
    assert rental.bike is bike, "Store the Bike object itself."
    assert rental.minutes == 40


def test_rental_prices_the_pairing():
    """Rental - the price belongs to the rental, not to either side"""
    ana = Member("Ana")

    assert Rental(ana, Bike("A1", "Grand Army", False), 40).price() == 10.00
    assert Rental(ana, Bike("A1", "Grand Army", False), 10).price() == 2.50


def test_rental_can_reach_through_to_either_side():
    """Rental - holding the objects means it can answer about both"""
    rental = Rental(Member("Ana"), Bike("A1", "Grand Army", False), 40)

    assert rental.member.name == "Ana"
    assert rental.bike.serial == "A1"
    assert rental.bike.is_rentable() is True


def test_involves_asks_about_identity_not_names():
    """Rental - two members with one name are still two members"""
    ana = Member("Ana")
    other_ana = Member("Ana")
    rental = Rental(ana, Bike("A1", "Grand Army", False), 40)

    assert rental.involves(ana) is True
    assert rental.involves(other_ana) is False, \
        "Compare with `is`, so a shared name does not count as the same member."


def test_rental_names_both_sides_when_printed():
    """Rental - __repr__ says which pairing you are holding"""
    rental = Rental(Member("Ana"), Bike("A1", "Grand Army", False), 40)

    assert repr(rental) == "Rental(Ana, A1)"


import pytest



def share():
    system = BikeShare()
    ana = Member("Ana")
    bike = Bike("A1", "Grand Army", False)
    system.add_member(ana)
    system.add_bike(bike)
    return system, ana, bike


def test_bikeshare_owns_its_collections_non_publicly():
    """BikeShare - both lists start empty and non-public on the instance"""
    system = BikeShare()
    lists = {name: value for name, value in vars(system).items()
             if isinstance(value, list)}

    assert len(lists) == 2, "Start two collections in __init__, one of each kind."
    assert all(name.startswith("_") for name in lists), \
        "Both collections are non-public, so callers go through the methods."
    assert all(value == [] for value in lists.values()), "Both start empty."


def test_bikeshare_reports_what_can_be_rented():
    """BikeShare - rentable_bikes offers the bikes that are available"""
    system, _, bike = share()

    assert system.rentable_bikes() == [bike]
    assert BikeShare().rentable_bikes() == []


def test_rentable_bikes_hands_back_a_new_list():
    """BikeShare - a caller editing the result cannot change the fleet"""
    system, _, _ = share()

    system.rentable_bikes().clear()

    assert len(system.rentable_bikes()) == 1, \
        "Return a new list, so clearing the result leaves the fleet alone."


def test_renting_works_when_every_rule_passes():
    """BikeShare - a registered member may take a bike in the fleet"""
    system, ana, bike = share()

    assert system.rent(ana, bike) == "Ana rented A1"
    assert system.rentable_bikes() == [], "The bike is out, so it is not on offer."


def test_each_rule_refuses():
    """BikeShare - unregistered member, bike not in the fleet, bike not available"""
    system, ana, bike = share()

    with pytest.raises(ValueError):
        system.rent(Member("Ben"), bike)

    with pytest.raises(ValueError):
        system.rent(ana, Bike("Z9", "Elsewhere", False))

    system.rent(ana, bike)
    with pytest.raises(ValueError):
        system.rent(ana, bike)


def test_a_refused_rental_changes_nothing():
    """BikeShare - the rules are all checked before anything moves"""
    system, _, bike = share()

    with pytest.raises(ValueError):
        system.rent(Member("Ben"), bike)

    assert system.rentable_bikes() == [bike], \
        "Check every rule before changing the system, so a refusal leaves it as it was."


import pytest



def repair():
    return Repair(Bike("A1", "Grand Army", True), "bent wheel")


def test_a_repair_starts_reported():
    """Repair - __init__ holds the bike, the fault and the first status"""
    job = repair()

    assert job.status == "reported"
    assert job.bike.serial == "A1"
    assert job.fault == "bent wheel"


def test_the_steps_run_in_order():
    """Repair - reported, then in_progress, then done"""
    job = repair()

    job.start()
    assert job.status == "in_progress"

    job.finish()
    assert job.status == "done"


def test_finishing_before_starting_is_refused():
    """Repair - finish raises from reported"""
    job = repair()

    with pytest.raises(ValueError):
        job.finish()

    assert job.status == "reported", "Refuse before moving the status."


def test_starting_twice_is_refused():
    """Repair - start raises from in_progress"""
    job = repair()
    job.start()

    with pytest.raises(ValueError):
        job.start()

    assert job.status == "in_progress"


def test_nothing_runs_once_the_repair_is_done():
    """Repair - both steps raise from done, and the status holds"""
    job = repair()
    job.start()
    job.finish()

    with pytest.raises(ValueError):
        job.start()
    with pytest.raises(ValueError):
        job.finish()

    assert job.status == "done"


def test_is_open_reports_whether_work_remains():
    """Repair - open until it is done"""
    job = repair()

    assert job.is_open() is True
    job.start()
    assert job.is_open() is True
    job.finish()
    assert job.is_open() is False


import pytest



def test_station_starts_empty_with_a_non_public_collection():
    """Station - the list of bikes is non-public"""
    station = Station("Grand Army", 2)

    assert station.count() == 0
    assert "_bikes" in attributes_set_on(station), \
        "Start the list as self._bikes, so callers go through the methods."


def test_docking_fills_the_station():
    """Station - count and has_room follow what is docked"""
    station = Station("Grand Army", 2)
    station.dock(Bike("A1", "Grand Army", False))

    assert station.count() == 1
    assert station.has_room() is True

    station.dock(Bike("A2", "Grand Army", False))
    assert station.has_room() is False


def test_a_full_station_refuses_another_bike():
    """Station - dock raises rather than going over capacity"""
    station = Station("Grand Army", 1)
    station.dock(Bike("A1", "Grand Army", False))

    with pytest.raises(ValueError):
        station.dock(Bike("A2", "Grand Army", False))

    assert station.count() == 1, "A refused dock must not add the bike."


def test_bikes_here_reports_what_is_docked():
    """Station - it lists the bikes it owns"""
    station = Station("Grand Army", 3)
    bike = Bike("A1", "Grand Army", False)
    station.dock(bike)

    assert station.bikes_here() == [bike]


def test_bikes_here_hands_back_a_copy():
    """Station - a caller cannot reach the station's own list"""
    station = Station("Grand Army", 2)
    station.dock(Bike("A1", "Grand Army", False))

    handed_out = station.bikes_here()
    handed_out.clear()
    handed_out.append(Bike("Z9", "Elsewhere", False))

    assert station.count() == 1, \
        "Return a new list, so editing the result cannot change the station."
    assert station.bikes_here()[0].serial == "A1"
