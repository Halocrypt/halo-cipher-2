from random import randint
from string import ascii_letters
from struct import pack
from util import (
    DICTIONARY,
    b64e,
    get_rotating_indice,
    predictable_seed,
    sum_ascii_codes,
)


def _pack(seed, buffer):
    return "".join(
        [
            "<S(0x4a70):",
            ((f"{seed}")),
            "(0x4a70)ES>",
            "<I(0x4a70):",
            ",".join(f"{i[0]}" for i in buffer),
            "(0x4a70)EI>",
            "<D(0x4a70):",
            (("".join(x[1] for x in buffer))),
            "(0x4a70)ED>",
        ]
    )


def encode(plain_text):
    vec = randint(1, 100)
    seed = (predictable_seed(plain_text) + 1) * vec
    bucket = []
    buffer = []
    for index, token in enumerate(plain_text):
        if token not in ascii_letters:
            buffer.append((0, token))
            continue
        if index % 2:
            buffer.append(
                get_rotating_indice(
                    DICTIONARY, ascii_letters.index(token) + (seed * (index + 1))
                )
            )
            bucket.append(token)
        else:
            buffer.append(None)
    ascii_sum = sum_ascii_codes(bucket)
    for index, token in enumerate(plain_text):
        if index % 2 or token not in ascii_letters:
            # these have been taken careof
            continue
        buffer[index] = get_rotating_indice(
            DICTIONARY, ascii_letters.index(token) + (seed * ascii_sum * (index + 1))
        )
    return _pack(seed, buffer)


if __name__ == "__main__":
    print(encode(input("Plain Text:\n")))