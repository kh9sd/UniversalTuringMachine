import sys
if "pytest" in sys.modules:
    import tests.testing_config as config
else:
    import config
from constants import *
import mconfig
import tape
MConfig = mconfig.MConfig
Tape = tape.Tape


def process_description_num(dn):
    """
    creates and returns a dict of m-configs from a description number

    dn: string
        made up of numeric digits 1-7
        conversion to standard description by
        'A' by '1',
        'C' by '2',
        'D' by '3',
        'L' by '4',
        'R' by '5',
        'N' by '6',
        ';' by '7'
    """
    dn_convert_dict = {
        "1": "A",
        "2": "C",
        "3": "D",
        "4": "L",
        "5": "R",
        "6": "N",
        "7": ";"
    }

    for num_key in dn_convert_dict:
        dn = dn.replace(num_key, dn_convert_dict[num_key])

    return process_standard_des(dn)


def process_standard_des(sd):
    """
    creates and returns a dict of m-configs from a standard description

    sd: string
        made up of "D", "A", "C", "L", "R", "N", and ";", represents a TM
    """

    dct = {}

    chunks = sd.split(";")

    if chunks[-1] != "":
        raise ValueError("Failed parse, input doesn't end with ';' or 7")

    for chunk in chunks[:-1]:  # ignore last element, will be blank
        mcon = MConfig(chunk)
        if (mcon.name, mcon.symbol) not in dct:
            dct[(mcon.name, mcon.symbol)] = mcon
        else:
            raise ValueError("Failed m-config log, "
                             "duplicate m-config names and symbol")
    return dct


def master_process(in_sd):
    """
    processes input TM, checks if string or number and delegates afterwards
    returns a dictionary of MConfig

    in_sd: string
        either a standard description or description number of a Turing machine
    """

    if isinstance(in_sd, str):
        if in_sd.isnumeric():
            return process_description_num(in_sd)
        else:
            return process_standard_des(in_sd)
    else:
        raise TypeError("Input is not a str for DN or SD processing")


class TuringMachine:
    def __init__(self, mconfigs, tp=None, moves=0, c_mcon=None):
        self.mcons = master_process(mconfigs)

        if not tp:
            self.tape = Tape(config.tape_array, config.cur_pos)
        else:
            self.tape = tp
        self.moves = moves

        if not c_mcon:
            self.cur_mcon = self.mcons[(1, self.tape.get_symbol())]
        else:
            self.cur_mcon = c_mcon

    def get_mconfigs(self):
        """
        turns mconfig dict into nicely formatted string

        returns String
        """
        res = [f"{mcon}: {self.mcons[mcon]}" for mcon in self.mcons]
        return "\n".join(res)

    def get_tape(self):
        """
        turns tape into nicely formatted string

        returns String
        """
        return str(self.tape)

    def get_whole_state(self):
        """
        turns entire state of Turing machine in nicely formatted string
        displays current mcon, number of moves, and tape

        returns String
        """
        return f"Move {self.moves} on m-config: {self.cur_mcon.name}\n{self.tape}\n"

    def do_move(self):
        """
        actual running machine for the TM (UTM YEEEEEEEEEET)
        doesn't return anything, just runs the whole apply mcon and switches mcons
        will throw exceptions to catch if the TM halts at any point
        """
        print_sym, move_com = self.cur_mcon.operation

        self.tape.set_symbol(print_sym)
        self.tape.move(move_com)
        self.moves += 1

        try:
            self.cur_mcon = self.mcons[(self.cur_mcon.next, self.tape.get_symbol())]
        except KeyError:
            raise HaltedException("Failed transition, no match "
                                  "for given m-config and symbol!: "
                                  f"{self.cur_mcon.next} and  {self.tape.get_symbol()}")

    def __eq__(self, other):
        if not isinstance(other, TuringMachine):
            return False

        return self.tape == other.tape and \
            self.mcons == other.mcons and \
            self.moves == other.moves and \
            self.cur_mcon == other.cur_mcon


# example SDs and DNs
# DADDCRDAA;DAADDRDAAA;DAAADDCCRDAAAA;DAAAADDRDA; prints 0's and 1's right
#    31332531173113353111731113322531111731111335317
# DADDLDA;  prints blanks to the left
#    31334317
# DADDCLDA;  prints 0's to the left
#    313324317
# DADDCRDA;  prints 0's to the right
#    313325317
# DADDCCRDA; prints 1's to the right
#    3133225317
# DADDCNDAA;DAADCDCNDA;
# purposefully erroring TM
# DADDCRDAA;DADCDCLDAA;DAADDCLDA;DAADCDCRDAAA;
# 2-state, 2-symbol BB

