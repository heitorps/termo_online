import unicodedata

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



arq = open("palavras_big_clean.txt", "r")
palavras = []
for linha in arq:
    palavras.append(linha.removesuffix("\n"))
arq_dest = open("palavras_big_clean_2.txt", "w")
# palavras.sort()
for i, palavra in enumerate(palavras):
    print(i)
    for j, palavra2 in enumerate(palavras): 
        if(remove_acentos(palavra.strip().lower()) == remove_acentos(palavra2.strip().lower()) and i != j):
            print()
            palavras[j] = "______"

for palavra in palavras:
    if palavra != "______":
        arq_dest.write(palavra.strip().lower() + "\n")
arq.close()
arq_dest.close()