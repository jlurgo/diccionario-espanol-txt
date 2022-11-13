import json

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


todas_las_palabras = set()

with open("../../0_palabras_todas.txt") as fp:
    for line in fp:
        palabra = line.strip()
        todas_las_palabras.add(palabra)

print("Esperame un cachito...")
palabras_por_largo = {}
for palabra in todas_las_palabras:
    if len(palabra) not in palabras_por_largo:
        palabras_por_largo[len(palabra)] = []
    palabra_sin_acentos = palabra.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    palabras_por_largo[len(palabra)].append(palabra_sin_acentos)

if input(f"""
    Todas las palabras: {len(todas_las_palabras)}
    Palabras palabras_por_largo: {len(palabras_por_largo)}

    ¿Continuar? [y/N] """) != "y":
    exit()

# sort the dictionary by key (word length) in reverse order
palabras_por_largo = dict(sorted(palabras_por_largo.items(), key=lambda item: item[0], reverse=True))
for largo in palabras_por_largo:
    # sort the list of words alphabetically
    palabras_por_largo[largo].sort()

palindromes = {}
for largo_palabra in palabras_por_largo:
    if largo_palabra < 3:
        continue
    for i, palabra in enumerate(palabras_por_largo[largo_palabra]):
        # print if the inverted word is contained in any words of the set
        # also write to file
        printProgressBar(i, len(palabras_por_largo[largo_palabra]), prefix = f"Procesando palabras de largo {largo_palabra}:", suffix = f"Palabra {i}/{len(palabras_por_largo[largo_palabra])}", length = 50)
        palabra_invertida = palabra[::-1]
        for largo_busqueda in reversed(palabras_por_largo):
            if largo_busqueda < largo_palabra or largo_busqueda > largo_palabra + 4:
                continue
            for palabra_busqueda in palabras_por_largo[largo_busqueda]:
                if palabra_invertida in palabra_busqueda:
                    if palabra not in palindromes:
                        palindromes[palabra] = []
                    # append the word that contains the inverted word
                    # with the inverted word in capital letters
                    palindromes[palabra].append(palabra_busqueda.replace(palabra_invertida, palabra_invertida.upper()))
        if palabra in palindromes:
            print(f"{palabra} {palindromes[palabra]}")

with open('./palindromos.txt', 'w') as f:
    for pal in palindromes:
        line = f"{pal} : {palindromes[pal]}"
        f.write(line)
        f.write('\n')
    
with open('./palindromos.json', 'w') as f:
    json.dump(palindromes, f)

