def add_parity_bits(code_word: str, parity_size: int) -> str:
    new_word = ""
    for code in code_word:
        new_word += code * parity_size

    return new_word
