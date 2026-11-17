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


from debug import Checkout, Depot


TEST_SUITE_NAME = "Debug Tests"


import pytest



def test_appending_to_the_result_cannot_fill_the_depot():
    """Depot.contents - the caller gets a copy, not the depot's list"""
    depot = Depot("Yard", 2)
    depot.store("A1")

    depot.contents().append("A3")

    assert depot.count() == 1, "Return a new list so a caller cannot add to the depot."


def test_clearing_the_result_cannot_empty_the_depot():
    """Depot.contents - the other direction of the same bug"""
    depot = Depot("Yard", 2)
    depot.store("A1")

    depot.contents().clear()

    assert depot.count() == 1


def test_contents_still_reports_what_is_there():
    """Depot.contents - the copy holds the same items"""
    depot = Depot("Yard", 3)
    depot.store("A1")
    depot.store("A2")

    assert depot.contents() == ["A1", "A2"]
    assert Depot("Empty", 2).contents() == []


def test_store_was_left_alone():
    """Depot.store - the capacity rule was never the bug"""
    depot = Depot("Yard", 1)
    depot.store("A1")

    with pytest.raises(ValueError):
        depot.store("A2")

    assert "capacity" in code_of(Depot.store), \
        "store already enforced the capacity. The fix belongs in contents."


import pytest



def test_a_refused_completion_leaves_the_object_alone():
    """Checkout.complete - raising must not move the status or the total"""
    checkout = Checkout("Ana")

    with pytest.raises(ValueError):
        checkout.complete()

    assert checkout.status == "open", "Check the basket before assigning the status."
    assert checkout.total == 0
    assert checkout.items == []


def test_completing_a_real_basket_works():
    """Checkout.complete - the happy path is unchanged"""
    checkout = Checkout("Ana")
    checkout.add("A1", 4.00)
    checkout.add("A2", 2.50)

    assert checkout.complete() == 6.50
    assert checkout.status == "complete"
    assert checkout.total == 6.50


def test_a_refused_checkout_can_still_be_used():
    """Checkout.complete - this is what the bug cost"""
    checkout = Checkout("Ana")

    with pytest.raises(ValueError):
        checkout.complete()

    checkout.add("A1", 4.00)

    assert checkout.complete() == 4.00, \
        "A refused completion left the checkout open, so adding still works."


def test_add_was_left_alone():
    """Checkout.add - it already validated before changing anything"""
    checkout = Checkout("Ana")
    checkout.add("A1", 4.00)
    checkout.complete()

    with pytest.raises(ValueError):
        checkout.add("A2", 1.00)

    assert len(checkout.items) == 1
