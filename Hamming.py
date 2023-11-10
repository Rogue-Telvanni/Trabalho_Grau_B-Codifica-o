hamming_7_4_dict = {
    "0000000": "0000",
    "0001011": "0001",
    "0010111": "0010",
    "0011100": "0011",
    "0100110": "0100",
    "0101101": "0101",
    "0110001": "0110",
    "0111010": "0111",
    "1000101": "1000",
    "1000101": "1001",
    "1001110": "1001",
    "1010010": "1010",
    "1011001": "1011",
    "1100011": "1100",
    "1101000": "1101",
    "1110100": "1110",
    "1111111": "1111"
}

hamming_4_7_dict = {
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


def encode(stream: str) -> str:
    return hamming_4_7_dict[stream]


def decode(stream: str):
    parity_bits = stream[4: 7]
    code = stream[0: 4]
    # get the parityBits
    arr = []
    index = 0
    while len(arr) < len(parity_bits):
        selected = index + 1
        bit_1 = int(code[index])
        bit_2 = int(code[selected])
        if selected >= len(code) - 1:
            selected = selected - len(code)
        bit_3 = int(code[selected + 1])
        soma = bit_1 + bit_2 + bit_3
        bina = bin(soma)
        arr.append(bina[len(bina) - 1])
        index += 1

    # busca o bit com erro
    pos_erros = []
    corretas = []
    for i in range(len(arr)):
        if arr[i] != parity_bits[i]:
            pos_erros.append(i)
        else:
            corretas.append(i)

    if len(pos_erros) > 0 or len(corretas) > 0:
        if len(pos_erros) == 1:
            # o bit de paridade esta errado
            lista = list(parity_bits)
            lista[pos_erros[0]] = "1" if lista[pos_erros[0]] == "0" else "0"
            code = code + "".join(lista)
        elif len(pos_erros) == 2:
            value = corretas[0]
            match value:
                case 0:
                    codigo = list(code)
                    bit = bin(int(codigo[3]))
                    codigo[3] = bit[len(bit) - 1]
                    code = "".join(codigo) + parity_bits
                case 1:
                    codigo = list(stream)
                    bit = bin(int(codigo[0]))
                    codigo[0] = bit[len(bit) - 1]
                    code = "".join(codigo) + parity_bits
                case 2:
                    codigo = list(stream)
                    bit = bin(int(codigo[1]))
                    codigo[1] = bit[len(bit) - 1]
                    code = "".join(codigo) + parity_bits

            return hamming_7_4_dict[code]
    if stream in hamming_7_4_dict:
        return hamming_7_4_dict[stream]
    return stream
