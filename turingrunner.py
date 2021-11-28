import time
from mconfig import MConfig
import tape
Tape = tape.Tape


def display_mconfig_dict(m_dict):
    """
    for debug purposes, prints the m-configs in a dict

    m_dict: dictionary of m-configs
    """
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
        raise ValueError("Failed parse, input doesn't end with ';' or 7")

    for chunk in chunks[:-1]:  # ignore last element, will be blank
        mcon = MConfig(chunk)
        if (mcon.name, mcon.symbol) not in dict:
            dict[(mcon.name, mcon.symbol)] = mcon
        else:
            raise ValueError("Failed m-config log, "
                             "duplicate m-config names and symbol")
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
        raise TypeError("Input is not a str for DN or SD processing")


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

    # intitalizer for loop, only thing that matters is the q_1 next
    current_mcon = MConfig("DADDCRDA")

    while True:
        try:
            current_mcon = mdict[(current_mcon.next, tape.get_symbol())]
        except KeyError:
            raise KeyError("Failed transition, no match "
                           "for given m-config and symbol!: "
                           f"{current_mcon.next} and  {tape.get_symbol()}")

        print_com, move_com = current_mcon.operation
        tape.set_symbol(print_com[1:])
        tape.move(move_com)

        print(f"Current m-config: {current_mcon.name}")
        print(tape)

        time.sleep(0.75)


def tape_from_input(left_str, current_str, right_str, delimiter):
    """
    master function that calls process_tape and produce_tape

    Parameters:
        left_str: string
        current_str: string
        right_str: string
        delimiter: 1 character string

    Returns Tape object
    """
    return produce_tape(process_tape_input(left_str, delimiter),
                        current_str,
                        process_tape_input(right_str, delimiter))


def process_tape_input(input_str, delimiter):
    """
    processes string into array of strings, with user-defined delimiter

    Parameters:
        input_str: string
                   series of symbol separated by the delimiter that
                   represents a tape when read
        delimiter: 1 character string
                   defines separation between tape squares

    Returns array of strings, pre-trimmed with delimiter on both ends
    """
    input_list = input_str.strip(delimiter).split(delimiter)

    if len(input_list) == 1 and input_list[0] == "":
        return []
    return input_list


def produce_tape(left_input, current, right_input):
    """
    creates a Tape object, given tape to the left of the current square,
    the current square, and the tape to the right of the current square

    Parameters:
        left_input: array of strings
                    if no string passed from user, input is []
        right_input: same as left_input
        current: string

    Returns new Tape object, with current square set to the inputted square
    """

    # print(f"left: {left_input} right: {right_input} current: {current}")

    if left_input:
        left_tape = Tape()
        left_tape.set_symbol(left_input[0])

        for sym in left_input[1:]:
            left_tape.move_right()
            left_tape.set_symbol(sym)
    else:
        left_tape = None

    if right_input:
        right_tape = Tape()
        right_tape.set_symbol(right_input[-1])

        for sym in right_input[-2::-1]:  # traverses string excluding last, in reverse
            right_tape.move_left()
            right_tape.set_symbol(sym)
    else:
        right_tape = None

    current_tape = Tape()
    current_tape.set_symbol(current)

    if left_tape is not None:
        tape.join_tapes(left_tape, current_tape)

    if right_tape is not None:
        tape.join_tapes(current_tape, right_tape)

    # print(current_tape)

    return current_tape


def process_inputted_tape():
    if input("Do you want to have a starting tape? Y/N\n") == "Y":
        delimiter = input("What character will you separate your squares with?\n")

        left_str = input("Input the left side of the tape before the current square\n")

        current_str = input("Input the symbol on the current square\n")

        right_str = input("Input the right side of the tape after the current square\n")

        tp = tape_from_input(left_str, current_str, right_str, delimiter)
        print("Your starting tape is: ", tp)

        return tp
    else:
        return Tape()

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


if __name__ == "__main__":
    starting_tape = process_inputted_tape()

    input_sd = input("Enter your TM as a DN or SD: ")
    # input_sd = "DADDCRDAA;DAADDRDAAA;DAAADDCCRDAAAA;DAAAADDRDA;"

    try:
        mcons = master_process(input_sd)
    except ValueError as e:
        print("\nInvalid input for TM:\n", e)
        quit()

    try:
        run_tm(mcons, starting_tape)
    except KeyError as e:
        print("\nThis TM halted!\nReason:", e)
        quit()
