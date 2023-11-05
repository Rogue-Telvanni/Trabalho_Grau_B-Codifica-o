from enum import Enum

import Huffman
import BSC
import socket
import CRC

# constantes
BUFFER_SIZE = 2024
BSC_PARITY_SIZE = 3
Mode = Enum('Mode', ['CRC', 'BSC', 'Hamming'])


def main():
    stream = CRC.codify("100110")
    worked = CRC.validate(stream)

    choice = show_start()
    while choice == 0:
        show_start()

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
    mode = Mode('BSC')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            dados = input("digite a mensagem para enviar\n")
            if dados == "exit":
                break

            if dados in Mode:
                mode = Mode(dados)

            tree, sorted_symbols, code_word = Huffman.codify(dados)
            print("enviando code word" + code_word, end="\n")
            send_data = ""
            match mode.value:
                case 'BSC':
                    send_data = BSC.add_parity_bits(code_word, BSC_PARITY_SIZE)
                case 'CRC':
                    send_data = CRC.codify(code_word)

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
    mode = Mode('BSC')
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
                if dados in Mode:
                    mode = Mode(dados)
                    connection.sendall(("mudando para receber: " + mode.name).encode())
                    continue

                print("Recebi" + dados)
                split_str = dados.split("|")
                tree_string = split_str[0]
                code_word = split_str[1]
                print("Valor Recebido: " + code_word, end="\n")
                code_word = BSC.valida_bits(code_word, BSC_PARITY_SIZE)
                print("valor a ser decodificado: " + code_word, end="\n")
                dicio = dict()
                for value in tree_string.split("-"):
                    dicio[value.split(":")[0]] = int(value.split(":")[1])

                tree = Huffman.generate_tree(dicio)
                resultado = Huffman.decodify(tree, code_word)
                print("valor decodificado: " + resultado, end="\n")
                connection.sendall(("Recebi: " + resultado).encode())


if __name__ == '__main__':
    main()
