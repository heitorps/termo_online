import random

arq = open("palavras.txt", "r")
palavras = []
for linha in arq:
    palavras.append(linha.removesuffix("\n"))

print(palavras)

alvo = palavras[random.randint(0,999)]

