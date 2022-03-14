import sys
if "pytest" in sys.modules:
    import tests.testing_config as config
else:
    import config
from constants import *


class TapeSquare:
    """
    represents a single square on the tape of a Turing machine
    basically implemented as a linked list node
    """
    symbol_dict = config.sym_dict

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
        """

        if not lst:
            self.current = TapeSquare()
            return

        if pos >= len(lst):
            raise ValueError("Position is out of bounds of list (index starts at 0)")

        cur_sqr = sentinel_head = TapeSquare()

        for item in lst:
            cur_sqr.next = TapeSquare(item, prev=cur_sqr)
            cur_sqr = cur_sqr.next

        for i in range((len(lst) - 1) - pos):
            cur_sqr = cur_sqr.prev

        sentinel_head.next.prev = None
        self.current = cur_sqr

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

        if instruct == Move.STAY:
            pass
        elif instruct == Move.LEFT:
            self.move_left()
        elif instruct == Move.RIGHT:
            self.move_right()
        else:
            raise RuntimeError('Movement command is not "N", "L", or "R"')

    def traverse_end(self, go_left=True):
        holder = self.current
        if go_left:
            while holder.previous is not None:
                holder = holder.previous
        else:
            while holder.next is not None:
                holder = holder.next

        return holder

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

        return (left_str +
                "\033[4m" +
                f"[{self.current.data}]" +
                "\033[0m" +
                right_str)

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


def join_squares(left, right):
    if left.next is not None and right.prev is not None:
        raise AttributeError("Inputted squares aren't free on the sides")
    else:
        left.next = right
        right.prev = left


def join_tapes(left, right):
    """
    joins two tapes together, left and right respectively
    NOTE: THIS FUNCTION MODIFIES THE TAPES IN-PLACE
    """
    rightmost_left = left.traverse_end(False)
    leftmost_right = right.traverse_end(True)

    join_squares(rightmost_left, leftmost_right)
