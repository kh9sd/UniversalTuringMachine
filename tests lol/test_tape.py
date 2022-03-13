import pytest

from tape import *


@pytest.fixture
def example_tape_asd__def_shit():
    x, y, z = TapeSquare("asd"), TapeSquare("def"), TapeSquare("shit")

    x.next, y.prev = y, x
    y.next, z.prev = z, y

    bruh = Tape([], 0)

    bruh.current = y

    return bruh


@pytest.fixture
def example_tape__asd_def_shit():
    x, y, z = TapeSquare("asd"), TapeSquare("def"), TapeSquare("shit")

    x.next, y.prev = y, x
    y.next, z.prev = z, y

    bruh = Tape([], 0)

    bruh.current = x

    return bruh


@pytest.fixture
def example_tape_asd_def__shit():
    x, y, z = TapeSquare("asd"), TapeSquare("def"), TapeSquare("shit")

    x.next, y.prev = y, x
    y.next, z.prev = z, y

    bruh = Tape([], 0)

    bruh.current = z

    return bruh


@pytest.fixture
def example_blank_tape():
    TapeSquare.symbol_dict = {
        0: " ",
        1: "0",
        2: "1"
    }
    bruh = Tape([], 0)

    x = TapeSquare()

    bruh.current = x

    return bruh


def test_tape(example_tape_asd__def_shit, example_blank_tape):
    TapeSquare.symbol_dict = {
        0: " ",
        1: "0",
        2: "1"
    }
    # test constructor
    assert Tape(["asd", "def", "shit"], 1) == example_tape_asd__def_shit
    assert Tape([], 12321) == example_blank_tape


def test_get_symbol(example_tape_asd__def_shit, example_blank_tape):
    TapeSquare.symbol_dict = {
        0: " ",
        1: "0",
        2: "1"
    }
    assert example_tape_asd__def_shit.get_symbol() == "def"
    assert example_blank_tape.get_symbol() == " "


def test_set_symbol(example_tape_asd__def_shit, example_blank_tape):
    TapeSquare.symbol_dict = {
        0: " ",
        1: "0",
        2: "1"
    }

    a = example_tape_asd__def_shit
    a.set_symbol("LOL")
    assert a.get_symbol() == "LOL"

    b = example_blank_tape
    b.set_symbol("SHIT")
    assert b.get_symbol() == "SHIT"


def test_add_left(example_tape__asd_def_shit, example_blank_tape):
    TapeSquare.symbol_dict = {
        0: " ",
        1: "0",
        2: "1"
    }

    a = example_tape__asd_def_shit
    a.add_left()
    assert a == Tape([" ", "asd", "def", "shit"], 1)

    b = example_blank_tape
    b.add_left()
    assert b == Tape([" ", " "], 1)


def test_add_right(example_tape_asd_def__shit, example_blank_tape):
    TapeSquare.symbol_dict = {
        0: " ",
        1: "0",
        2: "1"
    }

    a = example_tape_asd_def__shit
    a.add_right()
    assert a == Tape(["asd", "def", "shit", " "], 2)

    b = example_blank_tape
    b.add_right()
    assert b == Tape([" ", " "], 0)


def test_move_left(example_tape_asd__def_shit, example_tape__asd_def_shit, example_blank_tape):
    TapeSquare.symbol_dict = {
        0: " ",
        1: "0",
        2: "1"
    }

    a = example_tape_asd__def_shit
    a.move_left()

    assert a == example_tape__asd_def_shit

    b = example_blank_tape
    b.move_left()

    assert b == Tape([" ", " "], 0)


def test_move_right(example_tape_asd__def_shit, example_tape_asd_def__shit, example_blank_tape):
    TapeSquare.symbol_dict = {
        0: " ",
        1: "0",
        2: "1"
    }

    a = example_tape_asd__def_shit
    a.move_right()
    assert a == example_tape_asd_def__shit

    b = example_blank_tape
    b.move_right()
    assert b == Tape([" ", " "], 1)


def test_move(example_tape_asd__def_shit, example_tape__asd_def_shit, example_tape_asd_def__shit):
    TapeSquare.symbol_dict = {
        0: " ",
        1: "0",
        2: "1"
    }

    a = example_tape_asd__def_shit
    a.move(Move.LEFT)
    assert a == example_tape__asd_def_shit
    a.move(Move.RIGHT)
    assert a == example_tape_asd__def_shit
    a.move(Move.STAY)
    assert a == example_tape_asd__def_shit
    a.move(Move.RIGHT)
    assert a == example_tape_asd_def__shit

    with pytest.raises(RuntimeError):
        a.move("shit")

    # fuck the blank tape


