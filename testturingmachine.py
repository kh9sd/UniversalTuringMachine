# import pygame


# turing machine
# assumes the only writes are 0 or 1 or e

# example SDs and DNs
# DADDCRDAA;DAADDRDAAA;DAAADDCCRDAAAA;DAAAADDRDA; prints 0's and 1's right
#    31332531173113353111731113322531111731111335317
# DADDLDA;  prints blanks to the left
#    31334317
# DADDCLDA;  prints 0's to the right
#    313324317
# DADDCRDA;  prints 0's to the right
#    313325317
# DADDCCRDA; prints 1's to the right
#    3133225317

sym_dict = {
    0: " ",
    1: "0",
    2: "1"
}

def SD_to_english(sd):
    for sd_chunk in sd.split(";"):
        chunk_to_english(sd_chunk)


def chunk_to_english(chk):
    # assuming its well behaved for now
    empty = []
    for char in chk:
        if char == "D":
            empty.append("")
        else:
            empty[-1] = empty[-1] + char

    empty[0] = "q" + str(len(empty[0]))
    empty[1] = symbol_to_english(empty[1])
    empty[2] = symbol_to_english(empty[2])
    empty[3] = "q" + str(len(empty[3]))
    return empty


def symbol_to_english(sym):
    if sym[-1] != "C":
        return sym_dict[len(sym[:-1])] + sym[-1]
    else:
        return sym_dict[len(sym)]


print(chunk_to_english("DADCDCCRDA"))
