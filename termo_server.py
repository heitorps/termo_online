#codigo do tcp/ip veio desse site https://pymotw.com/2/socket/tcp.html

import random
import unicodedata
import socket
import sys

########################################################################################################

def checaPalavra(inputStr : str, targetStr : str):
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
    for c in res:
        to_res += c
    return to_res
            
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

########################################################################################################

palavras = []
palavras_full = []
arq = open("palavras.txt", "r")
arq_full = open("palavras_big_clean_2.txt", "r")

for linha in arq:
    palavras.append(linha.removesuffix("\n"))
for linha in arq_full:
    palavras_full.append(linha.removesuffix("\n"))

while(True):
    diff = input("Escolha a dificuldade (facil/dificil)\n")

    if(diff == "facil"):
        alvo = palavras[random.randint(0,999)]
        break
    elif(diff == "dificil"):
        alvo = palavras_full[random.randint(0,5524)]
        break
    else:
        print("Dificuldade inválida")
        continue

########################################################################################################
def send_to_players(sckt1, sckt2, msg):
    sckt1.send(msg.encode('utf-8'))
    sckt2.send(msg.encode('utf-8'))


def game_action(connection):
    connection.send("Sua vez".encode('utf-8'))
    while(True):

        tentativa = connection.recv(1600).decode('utf-8')
        
        if(len(tentativa) != 5):
            # print("A palavra deve ter 5 letras")
            # continue
            connection.send("A palavra deve ter 5 letras".encode('utf-8'))
            continue
        
        achou = False
        for palavra in palavras_full:
            if(remove_acentos(palavra) == tentativa):
                tentativa_to_print = palavra
                achou = True
                break
        if(not achou):
            connection.send("A palavra não é válida (só tem 1000 palavras foi mal algumas vao ficar de fora)".encode('utf-8'))
            continue

        resultado = checaPalavra(tentativa, alvo)
        connection.send(stringEstado(tentativa_to_print, resultado).encode('utf-8'))
        if(resultado == "GGGGG"):
            return True
        return False

##################################################################################################

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 8081)
print ('starting up on %s port %s' % server_address)
sock.bind(server_address)
sock.listen(1)

# Wait for a connection
connection1, client_address1 = sock.accept()
nome1 = connection1.recv(1600).decode('utf-8')

connection2, client_address2 = sock.accept()
nome2 = connection2.recv(1600).decode('utf-8')

# while True:
    # data = connection1.recv(1600).decode('utf-8')
    # print (f'received {data}')
    # if data:
        # print ('sending data back to the client')
        # connection1.sendall(data.encode('utf-8'))
    # else:
        # print ('no more data from', client_address1)
        # break



for i in range(6):
    #send_to_players(connection1, connection2, f"Rodada {i+1}\n")
    # send_to_players(connection1, connection2, f"Vez de {nome1}\n")
    if game_action(connection1):
        # send_to_players(connection1, connection2, f"Jogador {nome1} venceu!\n A palavra era: {alvo}")
        exit(0)

    # send_to_players(connection1, connection2, f"Vez de {nome2}\n")
    if(game_action(connection2)):
        # send_to_players(connection1, connection2, f"Jogador {nome2} venceu!\n A palavra era: {alvo}")
        exit(0)
        
##################################################################################################


# i = 6
# while(i>0):
    # print(alvo)
    # tentativa = input()
    # if(len(tentativa) != 5):
        # print("A palavra deve ter 5 letras")
        # continue

    # achou = False
    # for palavra in palavras_full:
        # if(remove_acentos(palavra) == tentativa):
            # tentativa_to_print = palavra
            # achou = True
            # break
    # if(not achou):
        # print("A palavra não é válida (só tem 1000 palavras foi mal algumas vao ficar de fora)")
        # continue
    # 
    # i -= 1
    # resultado = checaPalavra(tentativa, alvo)
    # stringEstado(tentativa_to_print, resultado)
    # if(resultado == "GGGGG"):
        # print("Parabéns!")
        # exit(0)
# print(f"A palavra era {alvo}")