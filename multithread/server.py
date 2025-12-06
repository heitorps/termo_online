import threading
import socket
import sys
import random
import unicodedata

lock = threading.Lock()
turno_event = threading.Event() # Libera quando alguém pode jogar
tentativa_event = threading.Event() # Server recebeu uma tentativa
dados_tentativa = None # Compartilhado entre threads

alvo = ""
palavras_full = []

jogador_atual = 0 # 0 = A | 1 = B
# rodada = 1
# max_rodadas = 12
jogo_ativo = False


def envia(connection : socket.socket, msg):
    connection.sendall(msg.encode('utf-8'))

def remove_acentos(text):
    """
    Removes diacritical marks (accents, umlauts, etc.) from a string.

    Args:
    text (str): The input string.

    Returns:
    str: The string with diacritical marks removed.
    """
    normalized_text = unicodedata.normalize('NFKD', text)
    return "".join([c for c in normalized_text if not unicodedata.combining(c)])

def stringEstado(tentativa, resultado):
    out = ""
    BG_BLACK = "\033[40m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    RESET = "\033[0m"
    for i in range(5):
        if(resultado[i] == 'Y'):
            out += f"{BG_YELLOW}{tentativa[i]}{RESET}"
            #print(f"{BG_YELLOW}{tentativa[i]}{RESET}", end="")
        elif(resultado[i] == 'G'):
            out += f"{BG_GREEN}{tentativa[i]}{RESET}"
            #print(f"{BG_GREEN}{tentativa[i]}{RESET}", end="")
        else:
            out += f"{BG_BLACK}{tentativa[i]}{RESET}"
            #print(f"{BG_BLACK}{tentativa[i]}{RESET}", end="")
    
    return out


def checaPalavra(inputStr : str, targetStr : str, pontuacao):
    fTarget = remove_acentos(targetStr)
    res = ["W","W","W","W","W"]
    lCountTarget = {}
    lCountInput = {}
    for c in fTarget:
        lCountTarget[c] = lCountTarget.get(c,0) + 1
    
    for i in range(5):
        c = inputStr[i]
        if c == fTarget[i]:
            lCountInput[c] = lCountInput.get(c,0) + 1
            res[i] = 'G'

    for i in range(5):
        c = inputStr[i]
        if c == fTarget[i]:
            continue
        if c in fTarget and lCountInput.get(c,0) < lCountTarget.get(c,0):
            lCountInput[c] = lCountInput.get(c,0) + 1
            res[i] = 'Y'
        else: res[i] = 'W'

    to_res = ""
    old = pontuacao[jogador_atual]
    pontuacao[jogador_atual] = 0
    
    for c in res:
        to_res += c
        
        if c == 'G':
            pontuacao[jogador_atual] += 2
        elif c == 'Y':
            pontuacao[jogador_atual] += 1
    
    if(pontuacao[jogador_atual] == 10):
        pontuacao[jogador_atual] = old

    return to_res

def servidor_main():
    #escolhe a dificuldade e a palavra alvo
    # cria o socket do servidor
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', 8081)

    sock.bind(server_address)

    sock.listen(2)

    # aceita dois clientes
    client1, client_address1 = sock.accept()
    client2, client_address2 = sock.accept()

    # inicia threads para cada cliente e para o jogo
    threading.Thread(target=thread_cliente, args=(0, client1)).start()
    threading.Thread(target=thread_cliente, args=(1, client2)).start()
    threading.Thread(target=thread_jogo, args=(client1, client2)).start()


def thread_cliente(id_jogador, sock : socket.socket):
    global jogo_ativo, dados_tentativa, lock, jogador_atual, tentativa_event

    while not jogo_ativo: continue

    while jogo_ativo:
        msg = sock.recv(1024).decode('utf-8')
    
        if jogo_ativo:
            with lock:
                if id_jogador == jogador_atual:
                    dados_tentativa = (id_jogador, msg)
                    tentativa_event.set()

                else: sock.send("ESPERE SUA VEZ\n".encode('utf-8'))

        

    

def thread_jogo(client1, client2):
    global alvo, palavras_full
    print("Acessando base de palavras de Tel Aviv")

    palavras = []
    palavras_full = []
    arq = open("../palavras.txt", "r")
    arq_full = open("../palavras_big_clean_2.txt", "r")

    clients = []
    clients.append(client1)
    clients.append(client2)
    global jogo_ativo, jogador_atual, lock, turno_event, tentativa_event, dados_tentativa
    rodada = 1
    max_rodadas = 12
    ganhou = [False, False]
    pontuacao = [0,0]

    for linha in arq:
        palavras.append(linha.removesuffix("\n"))
    for linha in arq_full:
        palavras_full.append(linha.removesuffix("\n"))

    envia(client1, "Dificuldade (facil[0], dificil[1])\n")
    while(True):
        print("Pedindo dificuldade da tarefa da IDF")
        diff = client1.recv(1024).decode('utf-8')
        
        print(f"Solddado da IDF escolheu dificuldade {diff}")

        if "facil" in diff or "0" in diff:
            alvo = palavras[random.randint(0,999)]
            break
        elif "dificil" in diff or "1" in diff:
            alvo = palavras_full[random.randint(0,5524)]
            break
        else:
            envia(client1, "Dificuldade invalida\n")
            print("Dificuldade invalida")
            continue

    envia(client1, "ok\n")

    print("Pedindo Modo da tarefa da IDF")
    trans = False

    envia(client1, "Modo (invisivel[0]/visivel[1])\n")
    while(True):
        temp = client1.recv(1024).decode('utf-8')

        if "invisivel" in temp or "0" in temp:
            trans = False
            break
        elif(temp == "visivel" or temp == "1"):
            trans = True
            break
        else:
            print("Modo invalido")
            continue

    print(alvo)
    envia(client1, "ok\n")

    print("Mandando os soldados começarem")
    envia(client1, "start\n")
    envia(client2, "start\n")

    jogo_ativo = True
    f = True
    while jogo_ativo and rodada<=max_rodadas:  
        # print(clients)
        if f:
            envia(clients[jogador_atual], "SUA_VEZ\n")
            envia(clients[1 - jogador_atual], "AGUARDE\n")

        turno_event.set()

        tentativa_event.wait()
        tentativa_event.clear()

        with lock:
            jogador, tentativa = dados_tentativa

        cond, tentativa_to_print = checaValidadeTentativa(tentativa)
        if cond:
            envia(clients[jogador], "TENTATIVA INVALIDA\n")
            f = False
            continue
        f = True

        
        envia(clients[jogador], f"{stringEstado(str(tentativa_to_print), checaPalavra(tentativa, alvo, pontuacao))}\n")
        if trans:
            envia(clients[1 - jogador], f"O oponenente jogou: {str(tentativa_to_print)}\n")

        if tentativa_vencedora(tentativa):
            ganhou[jogador_atual] = True

        if rodada%2 == 0 and True in ganhou:
            if ganhou.count(True) == 2:
                if (pontuacao[0] > pontuacao[1]):
                    envia(clients[0], "VITORIA\n")
                    envia(clients[1], "DERROTA\n")
                elif (pontuacao[1] > pontuacao[0]):
                    envia(clients[1], "VITORIA\n")
                    envia(clients[0], "DERROTA\n")
                else:
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

def checaValidadeTentativa(tentativa):
    global palavras_full
    if len(tentativa) != 5:
        return True, ""
    
    achou = False
    for palavra in palavras_full:
        if(remove_acentos(palavra) == tentativa):
            tentativa_to_print = palavra
            achou = True
            break
    if(not achou):
        return True, ""
    
    return False, tentativa_to_print

def tentativa_vencedora(tentativa):
    if remove_acentos(tentativa) == remove_acentos(alvo):
        return True
    else: return False



if __name__ == "__main__":
    servidor_main()