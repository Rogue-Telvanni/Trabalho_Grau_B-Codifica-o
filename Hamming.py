hamming_7_4_dict = {
    "0000": "0000000",
    "0001": "0001011",
    "0010": "0010111",
    "0011": "0011100",
    "0100": "0100110",
    "0101": "0101101",
    "0110": "0110001",
    "0111": "0111010",
    "1000": "1000101",
    "1001": "1000101",
    "1001": "1001110",
    "1010": "1010010",
    "1011": "1011001",
    "1100": "1100011",
    "1101": "1101000",
    "1110": "1110100",
    "1111": "1111111",
}

"""adiciona os bits de paridade do algoritmo de hamming usando uma tabela pre definida"""


def haaming_7_4(stream: str) -> str:
    value = hamming_7_4_dict[stream]
    return stream + value

#def Validate(strea:str):

