import threading
import socket

inicio_jogo = False
fim_jogo = False

#lockInput = threading.Lock()

def main():
    global fim_jogo
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8080)

    sock.connect(server_address)
    

    threading.Thread(target=thread_receive, args=(sock, )).start()

    while not inicio_jogo:
        continue

    while not fim_jogo:
        msg = input()
        
        if(fim_jogo): break
        sock.send(msg.encode('utf-8'))

def thread_receive(sock: socket.socket):
    global fim_jogo, lockInput, inicio_jogo
    while not inicio_jogo:
        received = sock.recv(1024).decode('utf-8')
        print(received)

        if not received:
            break

        if received.startswith("Dificuldade"):
            while True: 
                diff = input()
                cert = sock.recv(1024).decode('utf-8')
                print(cert)
                if cert.endswith("ok"):
                    break
                sock.send(diff.encode('utf-8'))

        elif received.startswith("Modo"):
            while True:
                modo = input()
                cert = sock.recv(1024).decode('utf-8')
                print(cert)
                if cert.endswith("ok"):
                    inicio_jogo = True
                    break
                sock.send(modo.encode('utf-8'))

    while not fim_jogo:
        received = sock.recv(1024).decode('utf-8')

        if not received:
            break
        print(received)

        if received.endswith("(Digite qualquer coisa para sair)\n"):
            fim_jogo = True

        

        

if __name__ == "__main__":
    main()