from re import split

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
    return hamming_7_4_dict[stream]

def Validate(stream: str, parity_size: int):
    code = stream[0: len(stream) - parity_size]
    parity_bits = stream[len(code): len(code) + parity_size]
    # get the parityBits
    correct = hamming_7_4_dict[code][len(code): len(code) + parity_size]
    if correct == parity_bits:
        return
    else:
        arr = []
        index = 0
        while len(arr) < len(parity_bits):
            selected = index + 1
            while selected != len(code) - 1:
                bit_1 = int(code[index])
                bit_2 = int(code[selected])
                bit_3 = int(code[selected + 1])
                soma = bit_1 + bit_2 + bit_3
                bina = bin(soma)
                arr.append(bina[len(bina) - 1])
                selected += 1
            index += 1

        # busca o bit com erro
        pos_erros = []
        corretas = []
        for i in range(len(arr)):
            if arr[i] != parity_bits[i]:
                pos_erros.append(i)
            else:
                corretas.append(i)

        if len(pos_erros) == 1:
            # o bit de paridade esta errado
            lista = list(parity_bits)
            lista[pos_erros[0]] = "1" if lista[pos_erros[0]] == "0" else "0"
            return code + "".join(lista)
        elif len(pos_erros) == 2:
            value = corretas[0]
            match value:
                case 0:
                    codigo = list(code)
                    bit = bin(int(codigo[3]))
                    codigo[3] = bit[len(bit) - 1]
                    code = "".join(codigo)
                    return hamming_7_4_dict[code]
                case 1:
                    codigo = list(code)
                    bit = bin(int(codigo[0]))
                    codigo[0] = bit[len(bit) - 1]
                    code = "".join(codigo)
                    return hamming_7_4_dict[code]
                case 2:
                    codigo = list(code)
                    bit = bin(int(codigo[1]))
                    codigo[1] = bit[len(bit) - 1]
                    code = "".join(codigo)
                    return hamming_7_4_dict[code]
