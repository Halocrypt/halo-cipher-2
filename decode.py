from string import ascii_letters
from util import DICTIONARY, b64d, shift_array, sum_ascii_codes
from re import compile as re_compile, UNICODE
from struct import unpack


class CipherTextParser(object):
    def __init__(self, cipher_text, dictionary=DICTIONARY):
        self.cipher_text = cipher_text
        self.dictionary = dictionary

    parser_re = re_compile(
        r"""(?x)
        <S\(0x4a70\):
        (?P<seed>(.*))?
        \(0x4a70\)ES>
        <I\(0x4a70\):
        (?P<indices>(.*))?
        \(0x4a70\)EI>
        <D\(0x4a70\):
        (?P<encrypted_chunk>(.*))?
        \(0x4a70\)ED>
    """,
        UNICODE,
    )

    @classmethod
    def compile_cipher_text(self, cipher_text):
        match = self.parser_re.search(cipher_text)
        if not match:
            raise ValueError("Invalid cipher text")

        # the metadata
        seed = int(match.group("seed"))
        _indices = match.group("indices")
        indices = [int(_i) for _i in _indices.split(",") if _i]
        # the ACTUAL cipher

        encrypted_chunk = match.group("encrypted_chunk")
        return (seed, indices, encrypted_chunk)

    def _get_orig_ascii(self, indices, index, token):
        q = indices[index]
        mod = shift_array(self.dictionary, q).index(token)
        print(mod, q)
        orig = q * len(self.dictionary) + mod
        return orig

    def decode(self):
        seed, indices, encrypted_chunk = CipherTextParser.compile_cipher_text(
            self.cipher_text
        )
        bucket = []
        buffer = []
        for index, token in enumerate(encrypted_chunk):
            if token not in self.dictionary:
                buffer.append(token)
                continue
            if index % 2:
                orig = self._get_orig_ascii(indices, index, token)
                ascii_index = int(orig - (seed * (index + 1)))
                print(orig, seed, index, ascii_index, token)
                tmp = ascii_letters[ascii_index]
                buffer.append(tmp)
                bucket.append(tmp)
                continue
            else:
                buffer.append(None)

        ascii_sum = sum_ascii_codes(bucket)
        for index, token in enumerate(encrypted_chunk):
            if index % 2 or token not in self.dictionary:
                continue
            orig = self._get_orig_ascii(indices, index, token)
            ascii_index = int(orig - (seed * ascii_sum * (index + 1)))
            buffer[index] = ascii_letters[ascii_index]
        return "".join(buffer)


#


def decode(cipher_text, dictionary=DICTIONARY):
    klass = CipherTextParser(cipher_text, dictionary)
    return klass.decode()


if __name__ == "__main__":
    print(decode(input("Cipher Text:\n")))