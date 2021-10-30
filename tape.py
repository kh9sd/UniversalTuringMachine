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
            either "L", "R", or ""
            will move left, right, or not at all accordingly
        """

        if instruct == "":
            pass
        elif instruct == "L":
            self.move_left()
        elif instruct == "R":
            self.move_right()
        else:
            raise RuntimeError('Movement command is not " ", "L", or "R"')

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


input_sd = "DADDCRDAA;DAADDRDAAA;DAAADDCCRDAAAA;DAAAADDRDA;"
mconfig_dict = {}

# initialization, add mconfigs to dict
for chunk in input_sd.split(";")[:-1]:  # ignore last element, will be blank
    mconfig = MConfig(chunk)
    mconfig_dict[mconfig.name] = mconfig

# display_mconfig_dict(mconfig_dict)

current_mcon = mconfig_dict["q_1"]
# print_com, move_com = current_mcon.operation
# print(print_com)

# print(print_com[1:])
tape = Tape()
while True:
    if tape.square_check(current_mcon.symbol):
        print_com, move_com = current_mcon.operation
        tape.set_symbol(print_com[1:])
        tape.move(move_com)

        print(f"Current m-config: {current_mcon.name}")
        print(tape)

        current_mcon = mconfig_dict[current_mcon.next]
    else:
        raise RuntimeError("Tape's symbol doesn't match mconfig's")
    time.sleep(0.5)
