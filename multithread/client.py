import threading
import socket

fim_jogo = False

def main():
    global fim_jogo
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8081)

    sock.connect(server_address)

    threading.Thread(target=thread_resposta, args=(sock, )).start()

    while not fim_jogo:
        msg = input()
        #print(fim_jogo)
        if(fim_jogo): break
        sock.send(msg.encode('utf-8'))

def thread_resposta(sock: socket.socket):
    global fim_jogo
    while not fim_jogo:
        resposta = sock.recv(1024).decode('utf-8')

        if not resposta:
            break
        print(resposta, end="")
        if resposta.endswith("(Digite qualquer coisa para sair)\n"):
            fim_jogo = True
            print("Cabou o jogo")

if __name__ == "__main__":
    main()