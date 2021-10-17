class TapeSquare:
    """
    represents a square on the tape of a Turing machine
    basically a list node
    """
    def __init__(self, prev=None, next=None, data=" "):
        self.previous = prev
        self.next = next
        self.data = data

    # def __str__(self):
    #     return "(prev: {}, next: {}, data: {})".format(self.previous,
    #                                                    self.next,
    #                                                    self.data)


class Tape:
    """
    represents a tape object
    essentially a neutered doubly-linked list, in the spirit of Turing!
    also holds the current square on the tape, also in the spirit of Turing!
    """
    def __init__(self):
        self.head = TapeSquare()
        self.current = self.head

    def get_symbol(self):
        return self.current.data

    def set_symbol(self, sym):
        self.current.data = sym

    def add_left(self, parent):
        return TapeSquare(next=parent)

    def add_right(self, parent):
        return TapeSquare(prev=parent)

    def move_left(self):
        if self.current.previous is None:
            self.current.previous = self.add_left(self.current)
        self.current = self.current.previous

    def move_right(self):
        if self.current.next is None:
            self.current.next = self.add_right(self.current)
        self.current = self.current.next

    def __str__(self):
        # inefficient due to string immut, change later
        to_right = ""
        cur = self.current.next
        while cur is not None:
            to_right += f"[{cur.data}]"
            cur = cur.next

        to_left = ""
        cur = self.current.previous
        while cur is not None:
            to_left = f"[{cur.data}]" + to_left
            cur = cur.previous

        return (to_left +
                "\033[4m" +
                f"[{self.current.data}]" +
                "\033[0m" + to_right)
