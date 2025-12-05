import threading
import socket

inicio_jogo = False
fim_jogo = False

#lockInput = threading.Lock()

def main():
    global fim_jogo
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8081)

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
        received = sock.recv(1024).decode('utf-8').split("\n")
        for msg in received:
            if not msg or msg == "\n":
                continue

            print(msg)
            
            if msg.startswith("Dificuldade"):
                while True: 
                    diff = input("Dificuldade:")
                    sock.send(diff.encode('utf-8'))
                    
                    cert = sock.recv(1024).decode('utf-8')
                    if "ok" in cert:
                        break

            elif msg.startswith("Modo"):
                while True:
                    modo = input("Modo:")
                    sock.send(modo.encode('utf-8'))
                    
                    cert = sock.recv(1024).decode('utf-8')
                    
                    if "ok" in cert:
                        break

            elif "start" in msg:
                inicio_jogo = True

    print("Olha a partir daqui")
    while not fim_jogo:
        received = sock.recv(1024).decode('utf-8').split('\n')

        for msg in received:
            if not msg:
                break
            print(msg)

            if "sair" in msg:
                fim_jogo = True

        

        

if __name__ == "__main__":
    main()