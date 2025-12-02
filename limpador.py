arq = open("palavras_big.txt", "r")
palavras = []
for linha in arq:
    palavras.append(linha.removesuffix("\n"))
arq_dest = open("palavras_big_clean.txt", "w")
for palavra in palavras:
    palavra_limpa = palavra.strip().lower()
    if len(palavra_limpa) == 5 and palavra_limpa.isalpha():
        arq_dest.write(palavra_limpa + "\n")
arq.close()
arq_dest.close()