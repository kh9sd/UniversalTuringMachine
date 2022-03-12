import pytest

from mconfig import *


@pytest.fixture
def example_mconfig_data():
    ex = MConfig("DADDCRDA")  # (q_1, ' ', (P'1', R), q_1)

    return ex


def test_name_to_english():
    assert name_to_english("") == 0
    assert name_to_english("AAAA") == 4
    assert name_to_english("A") == 1


def test_symbol_to_english():
    MConfig.symbol_dict = {
        0: " ",
        1: "0",
        2: "1"
    }

    assert symbol_to_english("") == " "
    assert symbol_to_english("C") == "0"
    assert symbol_to_english("CC") == "1"


def test_oper_to_english():
    MConfig.symbol_dict = {
        0: " ",
        1: "0",
        2: "1"
    }

    assert oper_to_english("L") == (" ", "L")
    assert oper_to_english("CR") == ("0", "R")
    assert oper_to_english("CCN") == ("1", "N")


def test_verify():
    assert verify("DADDCRDA")
    assert verify("DAADDRDAAA")
    assert verify("DAADDNDAAA")
    assert verify("DADCDCLDAA")

    assert not verify("DADDCRDADA")
    assert not verify("DADDCRDAD")
    assert not verify("DADDCRD")
    assert not verify("DDDCRDA")
    assert not verify("DDDBGDA")


def test_name_check():
    assert name_check("AAA")
    assert name_check("A")

    assert not name_check("")
    assert not name_check("B")
    assert not name_check("BB")


def test_symbol_check():
    assert symbol_check("CCC")
    assert symbol_check("C")
    assert symbol_check("")

    assert not symbol_check("B")
    assert not symbol_check("A")
    assert not symbol_check("AB")


def test_operation_check():
    assert operation_check("L")
    assert operation_check("R")
    assert operation_check("N")
    assert operation_check("CL")
    assert operation_check("CR")
    assert operation_check("CN")
    assert operation_check("CCCL")
    assert operation_check("CCR")
    assert operation_check("CCN")

    assert not operation_check("")
    assert not operation_check("C")
    assert not operation_check("B")
    assert not operation_check("LL")
    assert not operation_check("BR")
    assert not operation_check("RN")
    assert not operation_check("CCLL")
    assert not operation_check("CECR")
    assert not operation_check("ECCN")


def test_next_check():
    assert next_check("AAA")
    assert next_check("A")

    assert not next_check("")
    assert not next_check("B")
    assert not next_check("BB")


def test_is_all_char():
    assert is_all_char("AAA", "A")
    assert is_all_char("A", "A")
    assert is_all_char("", "A")

    assert not is_all_char("AAB", "A")
    assert not is_all_char("BB", "A")
    assert not is_all_char("B", "A")
    assert not is_all_char("AAB", "A")
    assert not is_all_char("AAB", "B")


def test_mconfig(example_mconfig_data):
    MConfig.symbol_dict = {
        0: " ",
        1: "0",
        2: "1"
    }
    assert str(example_mconfig_data) == "('q_1', \"' '\", (\"P'0'\", 'R'), 'q_1')"
    # ('q_1', "' '", ("P'0'", 'R'), 'q_1')

