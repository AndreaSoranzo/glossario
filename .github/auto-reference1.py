import re

def creaGlossario(path):
    elenco_vocaboli = []
    with open(path,'r') as gloss:
        for line in gloss:
            x = re.search(r"\\subsection{", line)
            if x is not None:
                elenco_vocaboli.append(line[x.span()[1]:].strip())
                for i in range(len(elenco_vocaboli)):
                    elenco_vocaboli[i] = elenco_vocaboli[i].replace("}", "")
    elenco_vocaboli.sort(reverse = True)
    return elenco_vocaboli
   
def aggiungiG(path, elenco_vocaboli):
    with open(path, 'r', encoding='utf-8') as doc:
        """ with open(path, 'rb') as f:
        doc = f.read().replace(b'\x9d', b'\x22').replace(b'\x88', b'\xc3\xa8')
        first = doc.decode('utf-8', errors='ignore') """
        #print(first)
        first = re.sub(r"GitHub Pages[\\textsubscript{g}]?", str(elenco_vocaboli.index("GitHub Pages"))*10 + '0', doc.read())
    for word in elenco_vocaboli:
            #print(word, str(elenco_vocaboli.index(word))*10)
            first = re.sub(rf"(?<!section{{)\b{word.lower()}"+r"\\textsubscript{g}", str(elenco_vocaboli.index(word))*10 + '0', first)#, flags=re.IGNORECASE)
            first = re.sub(rf"(?<!section{{)\b{word}"+r"\\textsubscript{g}", str(elenco_vocaboli.index(word))*10 + '1', first)#, flags=re.IGNORECASE)
        #print(first)
        #print('\n\n')
    for word in elenco_vocaboli:
            #print(word, str(elenco_vocaboli.index(word))*10)
            first = re.sub(rf"(?<!section{{)\b{word.lower()}\b", str(elenco_vocaboli.index(word))*10 + '0', first)#, flags=re.IGNORECASE)
            first = re.sub(rf"(?<!section{{)\b{word}\b", str(elenco_vocaboli.index(word))*10 + '1', first)#, flags=re.IGNORECASE)
        #print( first)
    for i in range(len(elenco_vocaboli)-1, -1, -1):
            first = re.sub(str(i)*10 + '1', elenco_vocaboli[i]+r"\\textsubscript{g}", first)
            first = re.sub(str(i)*10 + '0', elenco_vocaboli[i].lower()+r"\\textsubscript{g}", first)

    with open(path, 'w', encoding='utf-8') as doc:
        doc.write(first)
        
#print(creaGlossario('01_intro.tex'))
#aggiungiG('titlepage.tex', creaGlossario('01_intro.tex'))
aggiungiG('content.tex', creaGlossario('01_intro.tex'))
