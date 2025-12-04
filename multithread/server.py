import threading
import socket
import sys

lock = threading.Lock()
turno_event = threading.Event() # Libera quando alguém pode jogar
tentativa_event = threading.Event() # Server recebeu uma tentativa
dados_tentativa = None # Compartilhado entre threads

jogador_atual = 0 # 0 = A | 1 = B
# rodada = 1
# max_rodadas = 12
jogo_ativo = True


def envia(connection : socket.socket, msg):
    connection.sendall(msg.encode('utf-8'))

def servidor_main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', 8081)

    sock.bind(server_address)

    sock.listen(2)

    # clients = []
    client1, client_address1 = sock.accept()
    client2, client_address2 = sock.accept()
    # clients.append(client1)
    # clients.append(client2)

    threading.Thread(target=thread_cliente, args=(0, client1)).start()
    threading.Thread(target=thread_cliente, args=(1, client2)).start()
    threading.Thread(target=thread_jogo, args=(client1, client2)).start()

    

def thread_cliente(id_jogador, sock : socket.socket):
    global jogo_ativo, dados_tentativa, lock, jogador_atual, tentativa_event
    while jogo_ativo:
        msg = sock.recv(1024).decode('utf-8')
    
        if jogo_ativo:
            with lock:
                if id_jogador == jogador_atual:
                    dados_tentativa = (id_jogador, msg)
                    tentativa_event.set()

                else: sock.send(b"ESPERE SUA VEZ")

    

def thread_jogo(client1, client2):
    clients = []
    clients.append(client1)
    clients.append(client2)
    global jogo_ativo, jogador_atual, lock, turno_event, tentativa_event, dados_tentativa
    rodada = 1
    max_rodadas = 12
    ganhou = [False, False]
    while jogo_ativo and rodada<=max_rodadas:  
        # print(clients)
        envia(clients[jogador_atual], "SUA_VEZ\n")
        envia(clients[1 - jogador_atual], "AGUARDE\n")

        turno_event.set()

        tentativa_event.wait()
        tentativa_event.clear()

        with lock:
            jogador, tentativa = dados_tentativa

        if tentativa_invalida(tentativa):
            envia(clients[jogador], "TENTATIVA INVALIDA\n")
            continue

        if tentativa_vencedora(tentativa):
            ganhou[jogador_atual] = True

        envia(clients[jogador], f"{str(tentativa).upper()}\n")

        if rodada%2 == 0 and True in ganhou:
            if ganhou.count(True) == 2:
                envia(clients[jogador], "EMPATE (ambos acertaram juntos)\n")
                envia(clients[1 - jogador], "EMPATE (ambos acertaram juntos)\n")

            else:
                ganhador = ganhou.index(True)
                envia(clients[ganhador], "VITORIA\n")
                envia(clients[1 - ganhador], "DERROTA\n")

            jogo_ativo = False

        jogador_atual = 1 - jogador_atual
        rodada +=1
    
    if jogo_ativo:
        envia(clients[jogador], "EMPATE (ambos perderam)\n")
        envia(clients[1 - jogador], "EMPATE (ambos perderam)\n")
        jogo_ativo = False

    envia(clients[jogador], "FIM (Digite qualquer coisa para sair)\n")
    envia(clients[1 - jogador], "FIM (Digite qualquer coisa para sair)\n")

def tentativa_invalida(tentativa):
    if tentativa == "oi":
        return True
    else: return False

def tentativa_vencedora(tentativa):
    if tentativa == "tchau":
        return True
    else: return False

if __name__ == "__main__":
    servidor_main()