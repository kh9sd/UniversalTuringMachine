# main event loop for turing machine
from mconfig import MConfig
from tape import Tape


def display_mconfig_dict(m_dict):
    for mcon in m_dict:
        print("{}: {}".format(mcon, mconfig_dict[mcon]))


input_sd = "DADDCRDAA;DAADDRDAAA;DAAADDCCRDAAAA;DAAAADDRDA;"

mconfig_dict = {}

position = 0

tape = Tape()

for chunk in input_sd.split(";")[:-1]:  # ignore last element, will be blank
    mconfig = MConfig(chunk)

    mconfig_dict[mconfig.get_name()] = mconfig

display_mconfig_dict(mconfig_dict)
