# main event loop for turing machine
# TODO: can I put this entirely into the tape.py?
import time
from mconfig import MConfig
from tape import Tape


def display_mconfig_dict(m_dict):
    for mcon in m_dict:
        print("{}: {}".format(mcon, mconfig_dict[mcon]))


input_sd = "DADDCRDAA;DAADDRDAAA;DAAADDCCRDAAAA;DAAAADDRDA;"
mconfig_dict = {}

# initialization, add mconfigs to dict
for chunk in input_sd.split(";")[:-1]:  # ignore last element, will be blank
    mconfig = MConfig(chunk)
    mconfig_dict[mconfig.name] = mconfig

# display_mconfig_dict(mconfig_dict)

current_mcon = mconfig_dict["q_3"]
# print_com, move_com = current_mcon.operation
# print(print_com)

# print(print_com[1:])
tape = Tape()
while True:
    if tape.square_check(current_mcon.symbol):
        print_com, move_com = current_mcon.operation

        tape.set_symbol(print_com[1:])

        tape.move(move_com)

        print(tape)
        current_mcon = mconfig_dict[current_mcon.next]
    else:
        raise RuntimeError("Tape's symbol doesn't match mconfig's")
    time.sleep(0.5)
