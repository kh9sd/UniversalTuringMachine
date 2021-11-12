import time
from mconfig import MConfig


class TapeSquare:
    """
    represents a single square on the tape of a Turing machine
    basically implemented as a linked list node
    """

    def __init__(self, prev=None, next=None, data=" "):
        """
        previous : another TapeSuare
            reference to the next TS to the left
        next: another TapeSquare
            reference to the next TS to the right
        data: string
            symbol stored on the TSquare
        """

        self.previous = prev
        self.next = next
        self.data = data

    # def __str__(self):
    #     return "(prev: {}, next: {}, data: {})".format(self.previous,
    #                                                    self.next,
    #                                                    self.data)


class Tape:
    """
    represents a Tape object

    This is essentially a neutered doubly-linked list, in the spirit of Turing!
    It also holds the current square on the tape, also in the spirit of Turing!
    """

    def __init__(self):
        """
        initializes a totally blank tape

        current: TapeSquare
            holds the current TapeSquare the TM is processing
        """

        self.current = TapeSquare()

    def get_symbol(self):
        """
        getter method for symbol on current TapeSquare
        purely for typing convenience
        """

        return self.current.data

    def set_symbol(self, sym):
        """
        setter method for symbol on current TapeSquare
        purely for typing convenience
        """

        self.current.data = sym

    def add_left(self, parent):
        """
        adds a new TapeSquare to the left of the passed square
        can assume that this is also the leftmost square

        parent: TapeSquare we are attaching this new TS to on the left
        """

        return TapeSquare(next=parent)

    def add_right(self, parent):
        """
        adds a new TapeSquare to the right of the passed square
        can assume that this is also the rightmost square

        parent: TapeSquare we are attaching this new TS to on the right
        """

        return TapeSquare(prev=parent)

    def move_left(self):
        """
        moves the current TapeSquare left one square
        also handles if this is the leftmost square
        """

        if self.current.previous is None:
            self.current.previous = self.add_left(self.current)
        self.current = self.current.previous

    def move_right(self):
        """
        moves the current TapeSquare right one square
        also handles if this is the rightmost square
        """

        if self.current.next is None:
            self.current.next = self.add_right(self.current)
        self.current = self.current.next

    def square_check(self, sym):
        """
        checks if current square symbol is same as passed symbol

        returns a Boolean

        symbol: string
            symbol we are checking
        """

        return self.current.data == sym

    def move(self, instruct):
        """
        moves the current square according to instruction passed

        instruct: string
            either "L", "R", or "N"
            will move left, right, or not at all accordingly
        """

        if instruct == "N":
            pass
        elif instruct == "L":
            self.move_left()
        elif instruct == "R":
            self.move_right()
        else:
            raise RuntimeError('Movement command is not "N", "L", or "R"')

    def __str__(self):
        """
        creates and returns string presentation of entire Tape
        current square is indictated by underline under symbol
        """

        to_right = []
        cur = self.current.next
        while cur is not None:
            to_right.append(f"[{cur.data}]")
            cur = cur.next

        to_left = []
        cur = self.current.previous
        while cur is not None:
            to_left.append(f"[{cur.data}]")
            cur = cur.previous

        right_str = "".join(to_right)
        left_str = "".join(to_left[::-1])

        return (left_str +
                "\033[4m" +
                f"[{self.current.data}]" +
                "\033[0m" +
                right_str)


def display_mconfig_dict(m_dict):
    for mcon in m_dict:
        print("{}: {}".format(mcon, mconfig_dict[mcon]))


def process_description_num(dn):
    """
    creates and returns a dict of m-configs from a description number

    dn: natural number
        number made up of digits 1-7
        conversion to standard description by
        'A' by 1,
        'C' by 2,
        'D' by 3,
        'L' by 4,
        'R' by 5,
        'N' by 6,
        ';' by 7
    """
    dn_convert = {
        "1": "A",
        "2": "C",
        "3": "D",
        "4": "L",
        "5": "R",
        "6": "N",
        "7": ";"
    }

    dn = str(dn)
    holder = []

    for num in dn:
        holder.append(dn_convert[num])
    return process_standard_des("".join(holder))


def process_standard_des(sd):
    """
    creates and returns a dict of m-configs from a standard description

    sd: string
        made up of "D", "A", "C", "L", "R", "N", and ";", represents a TM
    """

    dict = {}

    for chunk in sd.split(";")[:-1]:  # ignore last element, will be blank
        mcon = MConfig(chunk)
        if mcon.name not in dict:
            dict[mcon.name] = mcon
        else:
            raise ValueError("Duplicate m-config name")

    return dict


# main method
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

input_sd = "DAADDCNDAA;DAAADCCDCNDA;"

if isinstance(input_sd, str):
    mconfig_dict = process_standard_des(input_sd)
elif isinstance(input_sd, int):
    mconfig_dict = process_description_num(input_sd)
else:
    raise TypeError("Input is not an int or str for DN or SD processing")

# display_mconfig_dict(mconfig_dict)
try:
    current_mcon = mconfig_dict["q_1"]
except KeyError:
    print("No intital (q_1) m-config to start!")
    quit()

tape = Tape()

while True:
    try:
        if tape.square_check(current_mcon.symbol):
            print_com, move_com = current_mcon.operation
            tape.set_symbol(print_com[1:])
            tape.move(move_com)

            print(f"Current m-config: {current_mcon.name}")
            print(tape)

            current_mcon = mconfig_dict[current_mcon.next]
        else:
            print("This TM halted because a failed symbol check!")
            break
        time.sleep(0.75)

    except KeyError:
        print("This TM halted because of missing m-configs!")
        break
