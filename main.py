import Huffman
import BSC
import socket


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
        s.sendall(b"Hello, world")
        data = s.recv(1024)

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
                data = connection.recv(1024)
                if not data:
                    break

                connection.sendall("Recebi")


if __name__ == '__main__':
    main()
