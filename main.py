from turingmachine import TuringMachine
import time
from constants import *

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
# DADDCRDAA;DADCDCLDAA;DAADDCLDA;DAADCDCRDAAA;
# 2-state, 2-symbol BB

if __name__ == "__main__":
    input_sd = input("Enter your TM as a DN or SD: ")
    # input_sd = "DADDCRDAA;DAADDRDAAA;DAAADDCCRDAAAA;DAAAADDRDA;"

    try:
        tm = TuringMachine(input_sd)
    except ValueError as e:  # first line throws error
        print("\nInvalid input for TM:\n", e)
        quit()

    try:
        while True:
            print(tm.get_whole_state())
            tm.do_move()
            time.sleep(0.75)
    except HaltedException as e:
        print(e)


