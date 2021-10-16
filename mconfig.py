symbol_dict = {
    0: " ",
    1: "0",
    2: "1"
}


def name_to_english(nm):
    return "q_" + str(len(nm))


def symbol_to_english(sym):
    return symbol_dict[len(sym)]


def oper_to_english(opr):
    if opr == "" or opr[-1] == "C":
        return symbol_to_english(opr), " "
    else:
        return symbol_to_english(opr[:-1]), opr[-1]


verify_set = {"D", "A", "C", "L", "R"}


def verify(sd):
    """a string is valid as a Standard Description if
    -only includes letters D,A,C,L,R
    -must start with D followed by some A's
    -must then have another D followed by some C's
    -must then have another D followed by some C's
        -only this chain of C's can be followed with a single L or R
    -must have another D followed by some A's"""

    # print("\ntesting {} now!".format(sd))

    letter_set = set(sd)

    if(letter_set.issubset(verify_set)):
        chunks = sd.split("D")

        return ((len(chunks) == 5) and  # check right number of D's
                (chunks[0] == "") and  # check no chars before D
                (name_check(chunks[1])) and
                (symbol_check(chunks[2])) and
                (operation_check(chunks[3])) and
                (next_check(chunks[4])))
    else:
        return False

    # if letter_set.issubset(verify_set):  # initial check for correct letters
    #     chunks = sd.split("D")
    #     # print(chunks)
    #
    #     if len(chunks) != 5:
    #         print("wrong number of D's")
    #         return
    #
    #     if chunks[0] != "":
    #         print("SD must start with D")
    #         return
    #
    #     if name_check(chunks[1]):
    #         if symbol_check(chunks[2]):
    #             if operation_check(chunks[3]):
    #                 if next_check(chunks[4]):
    #                     print("passed!")
    #                     return
    #                 else:
    #                     print("SD check failed")
    #                     return
    #             else:
    #                 print("operation check failed")
    #                 return
    #         else:
    #             print("symbol check failed")
    #             return
    #     else:
    #         print("SD name check failed")
    #         return
    # else:
    #     print("wrong letters")
    #     return


def name_check(chk):
    return is_all_char(chk, "A")


def symbol_check(chk):
    return is_all_char(chk, "C")


def operation_check(chk):
    if chk != "":
        if chk[-1] == "L" or chk[-1] == "R":
            return symbol_check(chk[:-1])
        else:
            return symbol_check(chk)
    else:
        return True


def next_check(chk):
    return is_all_char(chk, "A")


def is_all_char(str, char):
    for ch in str:
        if(ch != char):
            return False
    return True


assert(verify("DADDCRDAA"))
assert(verify("DADDCLDA"))
assert(not verify("DA"))
assert(not verify("ZDA"))
assert(not verify("DADA"))
assert(verify("DDDD"))
assert(verify("DADCCDD"))
assert(verify("DADCCDCLD"))
assert(verify("DADCCDCRD"))
assert(verify("DADCCDCD"))


class MConfig:
    """
     represents m-configuration object
     holds current m-config, symbol to scan, operation, and next m-config
    """
    # ex. DADDCLDA, all ;'s already removed'

    def __init__(self, sd):
        if not verify(sd):
            raise ValueError("Invalid Standard Description for m-config")

        holder = []
        for char in sd:
            if char == "D":
                holder.append("")
            else:
                holder[-1] = holder[-1] + char

        self.name = name_to_english(holder[0])
        self.symbol = symbol_to_english(holder[1])
        self.operation = oper_to_english(holder[2])
        self.next = name_to_english(holder[3])
        # self.name, self.sym, self.oper, self.next = ("q_1", " ",
        #                                                   ("P0", "R"), "q_1")
        # name is something like q_1 or q_2
        # symbol is something like 0, 1, or " "
        # operation is a tuple like ("P0", "L")
        # first element starts with P for print, then a symbol
        # second element is movement, either "L", "R", or ""
        # next is the name of another m-config

    def __str__(self):
        return str((self.name, self.symbol, self.operation, self.next))

    def get_name(self):
        return self.name

    def get_symbol(self):
        return self.symbol

    def get_operation(self):
        return self.operation

    def get_next(self):
        return self.next
