from math import ceil
from random import randint, seed

import Hamming
import Huffman
import BSC
import socket
import CRC
import EncodeType

# encode  bsc varios erros em varios bits ok
# hamming mostrar a posição do erro ok
# no hamming quando o tamanho final for menor que 4 adicionar a quantidade
# necessária para fechar zero, o servidor deve receber o valor e decodificar


# constants
BUFFER_SIZE = 2024
BSC_PARITY_SIZE = 3


def main():
    seed()
    choice = show_start()
    while choice == 0:
        choice = show_start()

    host, port = show_conn_params()
    match choice:
        case 1:
            run_as_client(host, port)
        case 2:
            run_as_server(port)


def show_conn_params() -> (str, int):
    host = input("Digite o ip do servidor ou deixe em branco se selecionou servidor\n")
    port = int(input("digite a porta de conexão\n"))
    return host, port


def show_start() -> int:
    print("Selecione um mode")
    print("cliente - 1")
    print("servidor - 2")
    selection = input()
    if selection != "1" and selection != "2":
        return 0
    return int(selection)


def run_as_client(host: str, port: int):
    mode = EncodeType.EncodeType.BSC
    simulate_error = False
    rep = 3
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            dados = input("digite a mensagem para enviar\n")
            if dados == "exit":
                break

            if dados in [member.name for member in EncodeType.EncodeType]:
                print("mudando encoding")
                match dados:
                    case 'BSC':
                        mode = EncodeType.EncodeType.BSC
                    case 'CRC':
                        mode = EncodeType.EncodeType.CRC
                    case 'Hamming':
                        mode = EncodeType.EncodeType.Hamming
                s.sendall(dados.encode())
                data = s.recv(BUFFER_SIZE)
                print("retornado: " + data.decode())
                continue

            if dados == "erro":
                simulate_error = not simulate_error
                if simulate_error:
                    print("Mudando para não adicionar um erro")
                else:
                    print("mudando para não adicionar um bit de erro")
                continue
            elif dados == "rep":
                rep = int(input("digite o numero de repetições do erro para BSC"))
                continue

            tree, sorted_symbols, code_word = Huffman.codify(dados)
            print("enviando code word: " + code_word + " de tamanho: " + str(len(code_word)), end="\n")
            send_data = ""
            match mode.name:
                case 'BSC':
                    send_data = BSC.add_parity_bits(code_word, BSC_PARITY_SIZE)
                    if simulate_error:
                        send_data = adicionar_erro(send_data, rep)
                case 'CRC':
                    send_data = CRC.codify(code_word)
                    if simulate_error:
                        send_data = adicionar_erro(send_data, 1)
                case 'Hamming':
                    count = ceil(len(code_word) / 4)
                    for index in range(count):
                        offset = 4
                        data = ""
                        if index == count - 1:
                            offset = len(code_word) - index * 4
                            valor = code_word[index * 4: index * 4 + offset]
                            size = 4 - offset
                            valor = "0" * size + valor
                            data += Hamming.encode(valor) + "|" + str(offset)
                        else:
                            data += Hamming.encode(code_word[index * 4: index * 4 + offset])

                        if simulate_error:
                            data = adicionar_erro(data, 1)

                        send_data += data

            # gera a string com o dicionário para gerar a arvore
            tree_string = ""
            for key, value in sorted_symbols.items():
                tree_string += key + ":" + str(value) + "-"

            # remove o ultimo valor
            tree_string = tree_string[0: len(tree_string) - 1]

            send_data = tree_string + "|" + send_data
            print("enviando dados " + send_data, end="\n")
            s.sendall(send_data.encode())
            data = s.recv(BUFFER_SIZE)
            print(f"Received {data!r}", end="\n")


def run_as_server(port: int):
    # server side
    mode = EncodeType.EncodeType.BSC
    ip_conn = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.bind((ip_conn, port))
        tcp_socket.listen()
        print("Esperando conexão")
        connection, addr = tcp_socket.accept()
        with connection:
            print(f"Conectado com; {addr}")
            while True:
                data = connection.recv(BUFFER_SIZE)
                if not data:
                    break

                dados = data.decode()
                print("Recebi: " + dados)
                if dados in [member.name for member in EncodeType.EncodeType]:
                    match dados:
                        case 'BSC':
                            mode = EncodeType.EncodeType.BSC
                        case 'CRC':
                            mode = EncodeType.EncodeType.CRC
                        case 'Hamming':
                            mode = EncodeType.EncodeType.Hamming

                    connection.sendall(("mudando para receber: " + mode.name).encode())
                    continue

                split_str = dados.split("|")
                tree_string = split_str[0]
                code_word = split_str[1]
                print("Valor Recebido: " + code_word, end="\n")
                valido = True
                match mode.name:
                    case 'BSC':
                        code_word = BSC.valida_bits(code_word, BSC_PARITY_SIZE)
                    case 'CRC':
                        valido, code_word = CRC.validate(code_word)
                    case 'Hamming':
                        count = ceil(len(code_word) / 7)
                        data = ""
                        for index in range(count):
                            offset = 7
                            if index == count - 1:
                                size = int(split_str[2])
                                valor = Hamming.decode(code_word[index * 7: index * 7 + offset])
                                data += valor[len(valor) - size: len(valor)]
                            else:
                                data += Hamming.decode(code_word[index * 7: index * 7 + offset])
                        code_word = data

                print("valor a ser decodificado: " + code_word, end="\n")
                dicio = dict()
                for value in tree_string.split("-"):
                    dicio[value.split(":")[0]] = int(value.split(":")[1])

                tree = Huffman.generate_tree(dicio)
                resultado = Huffman.decodify(tree, code_word)

                if valido:
                    print("valor decodificado: " + resultado, end="\n")
                    connection.sendall(("Recebi: " + resultado).encode())
                else:
                    print("valor decodificado com erro: " + resultado, end="\n")
                    connection.sendall(("Recebi com erro: " + resultado).encode())


def adicionar_erro(code_word: str, rep: int) -> str:
    print("adicionando :" + str(rep) + " bits de erro")
    flip = {"1": "0", "0": "1"}
    lista = list(code_word)
    for i in range(rep):
        index = randint(0, len(code_word))
        while index > len(lista) - 1:
            index = randint(0, len(code_word))
            print("index maior que a lista: " + str(index))

        lista[index] = flip[lista[index]]

    return "".join(lista)


if __name__ == '__main__':
    main()
