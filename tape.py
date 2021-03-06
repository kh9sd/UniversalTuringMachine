import sys
if "pytest" in sys.modules:
    import tests.testing_config as config
else:
    import config
from constants import *
from itertools import pairwise


class TapeSquare:
    """
    represents a single square on the tape of a Turing machine
    basically implemented as a linked list node
    """
    symbol_dict = config.SYMBOL_DICT

    def __init__(self, data=None, prev=None, nxt=None):
        """
        previous : another TapeSquare
            reference to the next TS to the left
        next: another TapeSquare
            reference to the next TS to the right
        data: string
            symbol stored on the TSquare
        """
        # setting data to symbol_dict[0] at the header doesn't re-evaluate the
        # argument if the dict changes
        if data is None:
            data = TapeSquare.symbol_dict[0]

        self.prev = prev
        self.next = nxt
        self.data = data

    def __str__(self):
        return "(prev: {}, next: {}, data: {})".format(id(self.prev),
                                                       id(self.next),
                                                       self.data)


class Tape:
    """
    represents a Tape object

    This is essentially a neutered doubly-linked list, in the spirit of Turing!
    It also holds the current square on the tape, also in the spirit of Turing!
    """

    def __init__(self, lst, pos):
        """
        initializes a totally blank tape

        current: TapeSquare
            holds the current TapeSquare the TM is processing

        Fields:
            current: TapeSquare on the tape
        """

        if not lst:
            self.current = TapeSquare()
            return

        if pos not in range(0, len(lst)):
            raise ValueError("Position is out of bounds of list (index starts at 0)")

        tape_lst = [TapeSquare(val) for val in lst]

        for back, front in pairwise(tape_lst):
            back.next = front
            front.prev = back

        self.current = tape_lst[pos]

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

    def add_left(self):
        """
        adds a new TapeSquare to the left of the passed square
        can assume that this is also the leftmost square

        parent: TapeSquare we are attaching this new TS to on the left
        """

        new_sqr = TapeSquare(nxt=self.current)
        self.current.prev = new_sqr

    def add_right(self):
        """
        adds a new TapeSquare to the right of the passed square
        can assume that this is also the rightmost square

        parent: TapeSquare we are attaching this new TS to on the right
        """

        new_sqr = TapeSquare(prev=self.current)
        self.current.next = new_sqr

    def move_left(self):
        """
        moves the current TapeSquare left one square
        also handles if this is the leftmost square
        """

        if self.current.prev is None:
            self.add_left()
        self.current = self.current.prev

    def move_right(self):
        """
        moves the current TapeSquare right one square
        also handles if this is the rightmost square
        """

        if self.current.next is None:
            self.add_right()
        self.current = self.current.next

    def move(self, instruct):
        """
        moves the current square according to instruction passed

        instruct: string
            either "L", "R", or "N"
            will move left, right, or not at all accordingly
        """

        if instruct == Move.STAY:
            pass
        elif instruct == Move.LEFT:
            self.move_left()
        elif instruct == Move.RIGHT:
            self.move_right()
        else:
            raise RuntimeError('Movement command is not "N", "L", or "R"')

    def square_check(self, sym):
        """
        checks if current square symbol is same as passed symbol
        returns a Boolean
        symbol: string
            symbol we are checking
        """

        return self.current.data == sym

    def __repr__(self):
        return str(self)

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
        cur = self.current.prev
        while cur is not None:
            to_left.append(f"[{cur.data}]")
            cur = cur.prev

        right_str = "".join(to_right)
        left_str = "".join(to_left[::-1])

        # return (left_str +
        #         "\033[4m" +
        #         f"[{self.current.data}]" +
        #         "\033[0m" +
        #         right_str)

        return "...]" + left_str + f"<<[{self.current.data}]>>" + right_str + "[..."

    def __eq__(self, other):
        if not isinstance(other, Tape):
            return False

        # start checking if ahead list matches
        cur_this = self.current
        cur_other = other.current

        while cur_this and cur_other:
            if cur_this.data != cur_other.data:
                return False

            cur_this, cur_other = cur_this.next, cur_other.next

        if cur_this or cur_other:  # both must be None
            return False

        # start checking if before list matches
        cur_this = self.current
        cur_other = other.current

        while cur_this and cur_other:
            if cur_this.data != cur_other.data:
                return False

            cur_this, cur_other = cur_this.prev, cur_other.prev

        if cur_this or cur_other:
            return False

        return True
