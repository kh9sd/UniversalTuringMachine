import pytest

from turingmachine import *


# import turingmachine as tm


@pytest.fixture
def example_infinite_0_1_right_SD():
    return "DADDCRDAA;DAADDRDAAA;DAAADDCCRDAAAA;DAAAADDRDA;"


@pytest.fixture
def example_infinite_0_1_right_DN():
    return "31332531173113353111731113322531111731111335317"


@pytest.fixture
def example_infinite_0_1_right_mconfigs():
    return {(1, " "): MConfig("DADDCRDAA"),
            (2, " "): MConfig("DAADDRDAAA"),
            (3, " "): MConfig("DAAADDCCRDAAAA"),
            (4, " "): MConfig("DAAAADDRDA")}


@pytest.fixture
def example_halting_SD():
    return "DADDCNDAA;DAADCDCNDA;"


@pytest.fixture
def example_2_state_2_sym_BB_SD():
    return "DADDCRDAA;DADCDCLDAA;DAADDCLDA;DAADCDCRDAAA;"


@pytest.fixture
def example_BB_mconfigs():
    return {(1, " "): MConfig("DADDCRDAA"),
            (1, "0"): MConfig("DADCDCLDAA"),
            (2, " "): MConfig("DAADDCLDA"),
            (2, "0"): MConfig("DAADCDCRDAAA")}


@pytest.fixture
def example_inf_0_1_right_TM(example_infinite_0_1_right_SD):
    return TuringMachine(example_infinite_0_1_right_SD)


@pytest.fixture
def example_inf_0_1_TM_starter(example_infinite_0_1_right_DN):
    return TuringMachine(example_infinite_0_1_right_DN, Tape(["among", "us", " "], 2), 2)


def test_process_description_num(example_infinite_0_1_right_DN, example_infinite_0_1_right_mconfigs):
    assert process_description_num(example_infinite_0_1_right_DN) == example_infinite_0_1_right_mconfigs


def test_process_standard_des(example_infinite_0_1_right_SD, example_infinite_0_1_right_mconfigs):
    assert process_standard_des(example_infinite_0_1_right_SD) == example_infinite_0_1_right_mconfigs


def test_master_process(example_infinite_0_1_right_SD,
                        example_infinite_0_1_right_DN,
                        example_infinite_0_1_right_mconfigs):
    assert master_process(example_infinite_0_1_right_SD) == example_infinite_0_1_right_mconfigs
    assert master_process(example_infinite_0_1_right_DN) == example_infinite_0_1_right_mconfigs

    # no trailing semi/7
    with pytest.raises(ValueError):
        master_process("DADDCRDAA;DADCDCLDAA;DAADDCLDA;DAADCDCRDAAA")

    with pytest.raises(ValueError):
        master_process("3133253117311335311173111332253111173111133531")

    # wrong type for DN
    with pytest.raises(ValueError):
        master_process(3133253117311335311173111332253111173111133531)


def test_get_mconfigs(example_inf_0_1_right_TM, example_infinite_0_1_right_mconfigs):
    assert example_inf_0_1_right_TM.get_mconfigs() == """(1, \' \'): (\'q_1\', "\' \'", ("P\'0\'", \'R\'), \'q_2\')
(2, \' \'): (\'q_2\', "\' \'", ("P\' \'", \'R\'), \'q_3\')
(3, \' \'): (\'q_3\', "\' \'", ("P\'1\'", \'R\'), \'q_4\')
(4, \' \'): (\'q_4\', "\' \'", ("P\' \'", \'R\'), \'q_1\')"""


def test_get_tape(example_inf_0_1_right_TM, example_inf_0_1_TM_starter):
    assert example_inf_0_1_right_TM.get_tape() == "\033[4m" + "[ ]" + "\033[0m"
    assert example_inf_0_1_TM_starter.get_tape() == "[among][us]" + "\033[4m" + "[ ]" + "\033[0m"


def test_get_whole_state(example_inf_0_1_right_TM, example_inf_0_1_TM_starter):
    assert example_inf_0_1_right_TM.get_whole_state() == \
           """Move 0 on m-config: 1
\033[4m[ ]\033[0m
"""

    assert example_inf_0_1_TM_starter.get_whole_state() == \
           """Move 2 on m-config: 1
[among][us]\033[4m[ ]\033[0m
"""


def test_do_move(example_2_state_2_sym_BB_SD, example_BB_mconfigs):
    a = TuringMachine(example_2_state_2_sym_BB_SD)
    assert a == TuringMachine(example_2_state_2_sym_BB_SD, None, 0, 1)

    a.do_move()
    assert a == TuringMachine(example_2_state_2_sym_BB_SD,
                              Tape(["0", " "], 1),
                              1,
                              2)
    a.do_move()
    assert a == TuringMachine(example_2_state_2_sym_BB_SD,
                              Tape(["0", "0"], 0),
                              2,
                              1)
    a.do_move()
    assert a == TuringMachine(example_2_state_2_sym_BB_SD,
                              Tape([" ", "0", "0"], 0),
                              3,
                              2)
    a.do_move()
    assert a == TuringMachine(example_2_state_2_sym_BB_SD,
                              Tape([" ", "0", "0", "0"], 0),
                              4,
                              1)
    a.do_move()
    assert a == TuringMachine(example_2_state_2_sym_BB_SD,
                              Tape(["0", "0", "0", "0"], 1),
                              5,
                              2)

    a.do_move()
    assert a == TuringMachine(example_2_state_2_sym_BB_SD,
                              Tape(["0", "0", "0", "0"], 2),
                              6,
                              3)

    with pytest.raises(HaltedException):
        a.do_move()

    b = TuringMachine(example_2_state_2_sym_BB_SD, Tape(["1", "0"], 0))
    with pytest.raises(HaltedException):
        b.do_move()
