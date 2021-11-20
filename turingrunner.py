import time
from mconfig import MConfig
from tape import Tape


def display_mconfig_dict(m_dict):
    for mcon in m_dict:
        print("{}: {}".format(mcon, m_dict[mcon]))


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

    dict = {}

    chunks = sd.split(";")

    if chunks[-1] != "":
        # raise ValueError("Failed parse, input doesn't end with ';' or 7")
        print("Failed parse, input doesn't end with ';' or 7")
        quit()

    for chunk in chunks[:-1]:  # ignore last element, will be blank
        mcon = MConfig(chunk)
        if mcon.name not in dict:
            dict[mcon.name] = mcon
        else:
            # raise ValueError("Duplicate m-config name")
            print("Failed m-config logging, duplicate m-config names")
            quit()

    return dict


def master_process(in_sd):
    """
    processes input TM, checks if string or number and delegates afterwards
    returns a dictionary of MConfig

    in_sd: int or string
        either a standard description or description number of a Turing machine
    """

    if isinstance(in_sd, str):
        if in_sd.isnumeric():
            return process_description_num(in_sd)
        else:
            return process_standard_des(in_sd)
    else:
        raise TypeError("Input is not an int or str for DN or SD processing")


def run_tm(mdict, tp=Tape()):
    """
    actual running machine for the TM (UTM YEEEEEEEEEET)
    doesn't return anything, just prints the formatted TM after each move
    will throw exceptions to catch if the TM halts at any point

    mdict: dictionary of MConfigs
        the stuff we need to run the TM
        while we know they are formatted correctly, might still halt

    tp: tape
        the thing the TM prints on
        default is just an empty tape, can possibly input already filled tapes
    """

    tape = tp

    try:
        current_mcon = mdict["q_1"]
    except KeyError:
        raise KeyError("no intital (q_1) m-config to start")

    while True:
        if tape.square_check(current_mcon.symbol):
            print_com, move_com = current_mcon.operation
            tape.set_symbol(print_com[1:])
            tape.move(move_com)

            print(f"Current m-config: {current_mcon.name}")
            print(tape)

            try:
                current_mcon = mdict[current_mcon.next]
            except KeyError:
                raise KeyError("missing m-config")
        else:
            raise ValueError("failed symbol check")

        time.sleep(0.75)

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


input_sd = "DADDCRDAA;DAADDRDAAA;DAAADDCCRDAAAA;DAAAADDRDA;"

mcons = master_process(input_sd)

try:
    run_tm(mcons)
except ValueError as e:
    print("\nThis TM halted!\nReason:", e)
except KeyError as e:
    print("\nThis TM halted!\nReason:", e)
