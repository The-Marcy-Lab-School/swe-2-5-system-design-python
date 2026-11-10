from modify import Book, BoroBikes, Delivery, Invoice, Library, Mechanic, Reader


TEST_SUITE_NAME = "Modify Tests"


def test_borobikes_still_tracks_the_fleet():
    """BoroBikes - the one job it keeps"""
    share = BoroBikes()
    share.add_bike("A1")
    share.add_bike("A2")

    assert share.fleet_size() == 2


def test_the_invoice_numbers_did_not_change():
    """Invoice - total moved, it did not get rewritten"""
    assert Invoice(40).total() == 10.00
    assert Invoice(10).total() == 2.50


def test_the_invoice_wording_did_not_change():
    """Invoice - text reads the same as before"""
    assert Invoice(40).text("Ana") == "Ana owes 10.0"


def test_the_mechanic_answers_for_itself():
    """Mechanic - priority and rota moved, and rota knows its own name"""
    mech = Mechanic("Sam")

    assert mech.priority("A1") == "normal"
    assert mech.priority("BROKEN-A1") == "urgent"
    assert mech.rota(2) == "Sam works 2 days"


def test_the_four_methods_left_borobikes():
    """BoroBikes - it is down to the fleet"""
    for name in ("invoice_total", "invoice_text", "repair_priority", "rota_for"):
        assert not hasattr(BoroBikes, name), \
            f"Delete {name} from BoroBikes. It belongs on another class now."


import pytest



def test_lending_records_the_loan_on_both_sides():
    """Library.lend - the coordinator updates the book and the reader"""
    library, ana, book = Library(), Reader("Ana"), Book("Dune")

    assert library.lend(ana, book) == "Ana borrowed Dune"
    assert book.on_loan is True
    assert ana.loan_count() == 1


def test_a_book_already_out_is_refused():
    """Library.lend - the availability rule"""
    library, book = Library(), Book("Dune")
    library.lend(Reader("Ana"), book)

    with pytest.raises(ValueError):
        library.lend(Reader("Ben"), book)


def test_the_loan_limit_is_enforced():
    """Library.lend - the rule Book.lend_to used to skip"""
    library, ana = Library(), Reader("Ana")
    for title in ["A", "B", "C"]:
        library.lend(ana, Book(title))

    with pytest.raises(ValueError):
        library.lend(ana, Book("D"))

    assert ana.loan_count() == 3


def test_a_refused_loan_changes_nothing():
    """Library.lend - check both rules before recording anything"""
    library, ana = Library(), Reader("Ana")
    for title in ["A", "B", "C"]:
        library.lend(ana, Book(title))

    extra = Book("D")
    with pytest.raises(ValueError):
        library.lend(ana, extra)

    assert extra.on_loan is False, "A refused loan must leave the book available."
    assert ana.loan_count() == 3


def test_the_two_back_doors_are_gone():
    """Library.lend - it is the only way to borrow now"""
    assert not hasattr(Book, "lend_to"), \
        "Delete Book.lend_to. It skipped the loan limit."
    assert not hasattr(Reader, "borrow"), \
        "Delete Reader.borrow. It skipped the availability check."


import pytest



def test_delivering_before_collecting_is_refused():
    """Delivery.deliver - the missing check"""
    job = Delivery("A1")

    with pytest.raises(ValueError):
        job.deliver()

    assert job.status == "packed", "Refuse before moving the status."


def test_the_right_order_still_works():
    """Delivery - packed, collected, delivered"""
    job = Delivery("A1")

    job.collect()
    assert job.status == "collected"

    job.deliver()
    assert job.status == "delivered"


def test_delivering_twice_is_refused():
    """Delivery.deliver - it also has to refuse from delivered"""
    job = Delivery("A1")
    job.collect()
    job.deliver()

    with pytest.raises(ValueError):
        job.deliver()

    assert job.status == "delivered"


def test_collecting_after_delivery_is_still_refused():
    """Delivery.collect - the transitions that were already right stay right"""
    job = Delivery("A1")
    job.collect()
    job.deliver()

    with pytest.raises(ValueError):
        job.collect()


def test_the_refusal_message_says_what_was_needed():
    """Delivery.deliver - the message matches the other two"""
    with pytest.raises(ValueError) as refusal:
        Delivery("A1").deliver()

    message = str(refusal.value)
    assert "collected" in message, "Name the status deliver needs."
    assert "packed" in message, "Name the status it found."
