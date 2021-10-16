symbol_dict = {
    0: " ",
    1: "0",
    2: "1"
}


class MConfig:
    """
     represents m-configuration object
     holds current m-config, symbol to scan, operation, and next m-config
    """

    def __init__(self, sd):
        self.name, self.sym, self.oper, self.next = ("q_1", " ", ("P0", "R"), "q_1")
        # name is something like q_1 or q_2
        # symbol is something like 0, 1, or " "
        # operation is a tuple like ("P0", "L")
        # first element starts with P for print, then a symbol
        # second element is movement, either "L", "R", or ""
        # next is the name of another m-config

    def __str__(self):
        return str((self.name, self.sym, self.oper, self.next))

    def process_sd(self, sd):
        # stub for DADDCRDA
        return ("q_1", " ", ("P0", "R"), "q_1")

    def get_name(self):
        return self.name
