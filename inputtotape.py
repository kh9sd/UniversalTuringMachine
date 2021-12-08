import tape

Tape = tape.Tape


def str_to_tape(input_str_arr, current_leftmost=True):
    """
    process an array of strings into a Tape object or None

    Parameters:
        input_str_arr: list of strings
            each element is a square on the tape
        current_leftmost: Boolean
            whether or not returned tape has either a reference to leftmost or
            rightmost square depending on user preference

    Returns Tape object, or None if input_str_arr is empty

    Examples:
        str_to_tape(["a", "b", "c"], current_leftmost=True) returns [a][b][c]
        str_to_tape(["a", "b", "c"], current_leftmost=False) returns [a][b][c]
    """
    if input_str_arr:
        tp = Tape()

        if current_leftmost:
            tp.set_symbol(input_str_arr[-1])  # set initial to rightmost char, then go left
            left_to_do = input_str_arr[-2::-1]  # traverses string excluding last, in reverse
        else:
            tp.set_symbol(input_str_arr[0])
            left_to_do = input_str_arr[1:]

        for sym in left_to_do:
            if current_leftmost:
                tp.move_left()
            else:
                tp.move_right()

            tp.set_symbol(sym)

        return tp
    else:
        return None


def join_left_cur_right(left_tape, cur_tape, right_tape):
    """
    modifies Tape objects in place and returns reference to current TapeSquare
    given tape to the left of the current square, the current square, and
    tape to the right of the current square

    Parameters:
        left_tape: Tape or None
        right_tape: Tape or None
        cur_tape: Tape
                one square Tape

    Returns new Tape object, with current square set to the inputted square
    """
    # print(f"left: {left_input} right: {right_input} current: {current}")

    if left_tape is not None:
        tape.join_tapes(left_tape, cur_tape)

    if right_tape is not None:
        tape.join_tapes(cur_tape, right_tape)

    return cur_tape


def process_tape_input(input_str, delimiter):
    """
    processes string into array of strings, with user-defined delimiter

    Parameters:
        input_str: string
                   series of symbol separated by the delimiter that
                   represents a tape when read
        delimiter: 1 character string
                   defines separation between tape squares

    Returns array of strings, pre-trimmed with delimiter on both ends
    """
    input_list = input_str.strip(delimiter).split(delimiter)

    if len(input_list) == 1 and input_list[0] == "":
        return []
    return input_list


def master_tape(left_str, current_str, right_str, delimiter):
    """
    master function that calls process_tape and produce_tape

    Parameters:
        left_str: string
        current_str: string
        right_str: string
        delimiter: 1 character string

    Returns Tape object
    """
    return join_left_cur_right(str_to_tape(process_tape_input(left_str, delimiter)),
                                           str_to_tape([current_str]),
                                           str_to_tape(process_tape_input(right_str, delimiter)))
