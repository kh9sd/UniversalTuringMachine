# main event loop for turing machine
from mconfig import MConfig
from tape import Tape

input_sd = "DADDCRDA;"

mconfig_dict = {}

tape = Tape()

for chunk in input_sd.split(";")[:-1]:  # ignore last element, will be blank
    mconfig = MConfig(chunk)

    mconfig_dict[mconfig.get_name()] = mconfig

print(mconfig_dict)
print(mconfig_dict["q_1"])
