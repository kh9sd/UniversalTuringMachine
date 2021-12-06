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


def produce_tape(left_input, current, right_input):
    """
    creates a Tape object, given tape to the left of the current square,
    the current square, and the tape to the right of the current square

    Parameters:
        left_input: array of strings
                    if no string passed from user, input is []
        right_input: same as left_input
        current: string

    Returns new Tape object, with current square set to the inputted square
    """
    # print(f"left: {left_input} right: {right_input} current: {current}")

    # whether or not the current square is right or leftmost doesn't matter for these
    left_tape = str_to_tape(left_input)
    right_tape = str_to_tape(right_input)

    current_tape = Tape()
    current_tape.set_symbol(current)

    if left_tape is not None:
        tape.join_tapes(left_tape, current_tape)

    if right_tape is not None:
        tape.join_tapes(current_tape, right_tape)

    # print(current_tape)
    return current_tape


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
    return produce_tape(process_tape_input(left_str, delimiter),
                        current_str,
                        process_tape_input(right_str, delimiter))

