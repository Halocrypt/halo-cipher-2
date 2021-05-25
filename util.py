from base64 import b64decode, b64encode
from collections import deque

DICTIONARY = "ΗΘअΚΞ🤣🤒ॠΝΠथ🤡αΛΟ💔ΩΜΡ😐इ🧠भΓΣऐΧΥΦढפּΙद🙊ΒΨ😤ड🐶🌏🍋Δ🏓💪Ε🕶ΖאΤ🤩😈ग"


def get_rotating_indice(heystack: str, index: int):
    length = len(heystack)
    q, r = divmod(index, length)
    return q, shift_array(heystack, q)[r]


def shift_array(arr, by):
    d = deque(arr)
    d.rotate(by)
    return d


def sum_ascii_codes(x):
    return sum(ord(i) for i in x)


def shift(*args):
    k = 1
    for i in args:
        k <= i
    return k


def predictable_seed(x):
    return shift(*(ord(i) for i in x))


def b64e(s):
    return b64encode(s)


def b64d(s):
    return b64decode(s)
