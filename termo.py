import random
import unicodedata

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
    print(res)
    for c in res:
        to_res += c
    print(to_res)
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

def printaEstado(tentativa, resultado):
    for i in range(5):
        if(resultado[i] == 'Y'):
            print(f"\033[33m{tentativa[i]}\033[0m", end="")
        elif(resultado[i] == 'G'):
            print(f"\033[32m{tentativa[i]}\033[0m", end="")
        else:
            print(f"\033[37m{tentativa[i]}\033[0m", end="")
    print("", end="\n")

########################################################################################################
palavras = []
palavras_full = []
arq = open("palavras.txt", "r")
arq_full = open("palavras_big_clean.txt", "r")

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
        alvo = palavras_full[random.randint(0,6025)]
        break
    else:
        print("Dificuldade inválida")
        continue
i = 6
while(i>0):
    print(alvo)
    tentativa = input()
    if(len(tentativa) != 5):
        print("A palavra deve ter 5 letras")
        continue

    achou = False
    for palavra in palavras_full:
        if(remove_acentos(palavra) == tentativa):
            saved = palavra
            achou = True
            break
    if(not achou):
        print("A palavra não é válida (só tem 1000 palavras foi mal algumas vao ficar de fora)")
        continue
    i -= 1
    resultado = checaPalavra(tentativa, alvo)
    printaEstado(saved, resultado)
    if(resultado == "GGGGG"):
        print("Parabéns!")
        exit(0)
print(f"A palavra era {alvo}")