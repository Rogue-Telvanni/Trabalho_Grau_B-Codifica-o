import collections


def add_parity_bits(code_word: str, parity_size: int) -> str:
    new_word = ""
    for code in code_word:
        new_word += code * parity_size

    return new_word


def valida_bits(bits: str, bsc_parity_size: int) -> str:
    code_word = ""
    for index in range(int(len(bits) / bsc_parity_size)):
        bit = bits[index * bsc_parity_size: index * bsc_parity_size + bsc_parity_size]
        code_word += collections.Counter(bit).most_common(1)[0][0]

    return code_word
