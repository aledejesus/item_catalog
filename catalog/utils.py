import random
import string

CHARS = string.ascii_letters + string.digits


def gen_ran_str(length):
    """
    Generate a random string of the specified length.
    Uses the characters in the CHARS list.

    Arguments:
        - length (int): desired string length

    Returns:
        - string: random string generated
    """
    return ''.join(random.choice(CHARS) for x in range(length))
