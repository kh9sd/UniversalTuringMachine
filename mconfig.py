"""
holds dict for conversion between number of C's after D to a symbol
"""
# TODO: make this more easier definable by the user
# also consider making symbol it's own class?
symbol_dict = {
    0: " ",
    1: "0",
    2: "1"
}


def name_to_english(nm):
    """
    makes an string representation of chain of A's passed from SD

    returns a string in the format of "q_{int}"
        int is determined by the length of the passed A's chain

    nm: string
        a string of pure A's (ex. "AAAAAA" or "") help
    """

    return "q_" + str(len(nm))


def symbol_to_english(sym):
    """
    makes a string representation of chain of C's passed from SD

    returns a symbol in the symbol_dict

    sym: string
        a string of pure C's (ex. "CCC" or "")
    """

    return symbol_dict[len(sym)]


def oper_to_english(opr):
    """
    makes a string representation of chain of C's possibly
    capped by a L or R from the SD

    returns a tuple formatted as
    ("P{symbol}"", move)
        where symbol is a symbol from the symbol_dict
        and move is a string, one of "L", "R", or ""

    opr: string
        chain of C's with a possible ending of L or R
        (ex. "CCCC" or "" or "L" "CR")
    """

    if opr == "" or opr[-1] == "C":
        return "P" + symbol_to_english(opr), ""
    else:
        return "P" + symbol_to_english(opr[:-1]), opr[-1]


"""
holds set of possible letters in SD
"""
verify_set = {"D", "A", "C", "L", "R"}


def verify(sd):
    """
    verifies whether a string passed is a valid Standard Description (SD)
        note: we've split the ;'s beforehand, so we dont check for them

    returns Boolean

    sd: string
        is valid as a Standard Description if
            only includes letters D,A,C,L,R
            must start with D followed by some A's
            must then have another D followed by some C's
            must then have another D followed by some C's
                only this chain of C's can be followed with a single L or R
            must have another D followed by some A's
    """

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


def name_check(chk):
    """
    checks if passed string from SD is all A's

    returns Boolean

    chk: string
        string that we're checking
    """

    return is_all_char(chk, "A")


def symbol_check(chk):
    """
    checks if passed string from SD is all C's

    returns Boolean

    chk: string
        string that we're checking
    """

    return is_all_char(chk, "C")


def operation_check(chk):
    """
    checks if passed string from SD is all C's, a slight exception if
    last char is L or R and rest is all C's

    returns Boolean

    chk: string
        string that we're checking
    """

    if chk != "":
        if chk[-1] == "L" or chk[-1] == "R":
            return symbol_check(chk[:-1])
        else:
            return symbol_check(chk)
    else:
        return True


def next_check(chk):
    """
    checks if passed string from SD is all A's

    returns Boolean

    chk: string
        string that we're checking
    """

    return is_all_char(chk, "A")


def is_all_char(str, char):
    """
    checks if passed str is entirely made up of passed char

    returns Boolean

    str: string
        the string we're checking
    char: string (one char)
        the char we're checking the string against
    """

    for ch in str:
        if(ch != char):
            return False
    return True

# assert(verify("DADDCRDAA"))
# assert(verify("DADDCLDA"))
# assert(not verify("DA"))
# assert(not verify("ZDA"))
# assert(not verify("DADA"))
# assert(verify("DDDD"))
# assert(verify("DADCCDD"))
# assert(verify("DADCCDCLD"))
# assert(verify("DADCCDCRD"))
# assert(verify("DADCCDCD"))


class MConfig:
    """
     represents m-configuration object

     a instruction for a Turing Machine
    """
    # ex. DADDCLDA, all ;'s already removed'

    def __init__(self, sd):
        """
        intializes an m-configuration object

        Takes in
        sd: string
            chunk of the Standard Description, split by the ;'s


        Fields:
        name: string
            name of the m-config
            formatted like q_{int} (ex. q_1)

        symbol: string
            symbol from the symbol_dict

        operation: tuple (string, string)
            first str formatted like "P{symbol}"
            second str is either "L", "R", or ""

        next: string
            name of the next M-Config


        Raises:
            ValueError if SD is not valid
        """

        if not verify(sd):
            raise ValueError("Invalid Standard Description for M-Config")

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

    def __str__(self):
        """
        creates and returns string representation of M-Config
        """
        return str((self.name, self.symbol, self.operation, self.next))
