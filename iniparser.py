def nline_strip(s):
    return s.replace("\n", "")


def parse(filename):
    """Returns a dict with int keys and string values"""
    return_dict = {}

    with open("config.ini", "r") as f:
        for line in f:
            line = nline_strip(line)

            if "=" in line:
                key, value = tuple(line.split("="))
                return_dict[int(key)] = value

    return return_dict
