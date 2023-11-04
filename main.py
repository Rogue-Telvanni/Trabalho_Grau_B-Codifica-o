import Huffman
import BSC
import socket
import collections

# constantes
BUFFER_SIZE = 2024
BSC_PARITY_SIZE = 3


def main():
    choice = show_start()
    while choice == 0:
        show_start()

    host, port = show_conn_params()
    match choice:
        case 1:
            run_as_client()
        case 2:
            run_as_server()


def show_conn_params() -> (str, int):
    host = input("Digite o ip do servidor")
    port = int(input("digite a porta de conexão"))
    return host, port


def show_start() -> int:
    print("Selecione um mode")
    print("cliente - 1")
    print("servidor - 2")
    selection = input()
    if selection != "1" or selection != "2":
        return 0
    return int(selection)


def run_as_client(host: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            dados = input("digite a mensagem para enviar")
            if dados == "exit":
                break

            tree, sorted_symbols, code_word = Huffman.codify(dados)
            send_data = BSC.add_parity_bits(code_word, BSC_PARITY_SIZE)
            # gera a string com o dicionário para gerar a arvore
            tree_string = ""
            for key, value in sorted_symbols.items():
                tree_string += key + ":" + str(value) + "-"

            # remove o ultimo valor
            tree_string = tree_string[0: len(tree_string) - 1]

            send_data = tree_string + "|" + send_data
            s.sendall(send_data)
            data = s.recv(BUFFER_SIZE)
            print(f"Received {data!r}")


def run_as_server():
    # server side
    port = 100
    ip_conn = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.bind((ip_conn, port))
        tcp_socket.listen()
        connection, addr = tcp_socket.accept()
        with connection:
            print(f"Conectado com; {addr}")
            while True:
                data = connection.recv(BUFFER_SIZE)
                if not data:
                    break

                split_str = data.split("|")
                tree_string = split_str[0]
                code_word = split_str[1]
                print("Valor Recebido: " + code_word)
                code_word = valida_bits(code_word)
                print("valor a ser decodificado: " + code_word)
                dicio = dict()
                for value in tree_string.split("-"):
                    dicio[value.split(":")[0]] = int(value.split(":")[1])

                tree = Huffman.generate_tree(dicio)
                resultado = Huffman.decodify(tree, code_word)
                print(resultado)
                connection.sendall("Recebi: " + resultado)


def valida_bits(bits: str) -> str:
    code_word = ""
    for index in range(int(len(bits) / BSC_PARITY_SIZE)):
        bit = bits[index * BSC_PARITY_SIZE: index * BSC_PARITY_SIZE + BSC_PARITY_SIZE]
        code_word += collections.Counter(bit).most_common(1)[0][0]

    return code_word


if __name__ == '__main__':
    main()
