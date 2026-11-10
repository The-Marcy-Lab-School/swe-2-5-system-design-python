from debug import Checkout, Depot


TEST_SUITE_NAME = "Debug Tests"


import inspect

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

    assert "capacity" in inspect.getsource(Depot.store), \
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
