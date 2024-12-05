import pathlib as path
import os
import concurrent.futures
import datetime 
import re

DOCS_PATH = "Docs"

def main(UseThread:bool=False):
    glox_path = path.Path(DOCS_PATH+"/Generali/glossario/01_intro.tex")

    defs = []
    ReadAllWords(glox_path,defs)

    if UseThread:
        with concurrent.futures.ThreadPoolExecutor(3) as pool: # with -> automatically wait for all threads
            for type in os.listdir(path.Path(DOCS_PATH)):
                if type == "Candidatura": # skippa la candidatura
                    continue
                pool.submit(Apply_g,defs,type)
    else:
        ApplyAll(defs) 


def ApplyAll(defs:list):
    for type in os.listdir(path.Path(DOCS_PATH)):
        if type == "Candidatura":
            continue
        Apply_g(defs, type)

def Apply_g(defs:list, type:str):
    for doc in os.listdir(path.Path(DOCS_PATH+"/"+type)):
        if doc == "glossario": # skippa il glossario
            continue
        if ("VE" in doc or "VI" in doc) and not IsRecent(doc): # skip old reports
            continue

        current_path = path.Path(DOCS_PATH+"/"+type+"/"+doc)
        for file in  os.listdir(current_path): # for each file file in a doc
            if ".tex" not in file: # if is not a tex file skip
                continue
            with open(str(current_path)+"/"+file,'r',encoding='utf-8') as f: #utf-8 per leggere virgolette strane o altri non ASCII
                first = re.sub(r"GitHub Pages[\\textsubscript{g}]?", str(defs.index("GitHub Pages"))*10 + '1', f.read()) #corner case
            for word in defs:
                """ controllo i termini già con il pedice distinguendo
                 se cominciano per maiuscola e minuscola; così evito di mettere
                 il pedice ai termini che sono tutti maiuscoli; e neanche ai
                 titoli delle sezioni """
                first = re.sub(rf"(?<!section{{)\b{word.lower()}"+r"\\textsubscript{g}", str(defs.index(word))*10 + '0', first) 
                first = re.sub(rf"(?<!subsection{{)\b{word.lower()}"+r"\\textsubscript{g}", str(defs.index(word))*10 + '0', first) 
                first = re.sub(rf"(?<!section{{)\b{word}"+r"\\textsubscript{g}", str(defs.index(word))*10 + '1', first)
                first = re.sub(rf"(?<!subsection{{)\b{word}"+r"\\textsubscript{g}", str(defs.index(word))*10 + '1', first)
            #print(first)
            for word in defs:
                """ controllo i termini senza il pedice, distinguendo
                 se cominciano per maiuscola e minuscola """
                first = re.sub(rf"(?<!section{{)\b{word.lower()}\b", str(defs.index(word))*10 + '0', first)
                first = re.sub(rf"(?<!subsection{{)\b{word.lower()}\b", str(defs.index(word))*10 + '0', first)
                first = re.sub(rf"(?<!section{{)\b{word}\b", str(defs.index(word))*10 + '1', first)
                first = re.sub(rf"(?<!subsection{{)\b{word}\b", str(defs.index(word))*10 + '1', first)
            #print( first)
            for i in range(len(defs)-1, -1, -1):
                """ risostituisco partendo dagli indici più alti, perché c'è
                 la possibilità che contengano sottostringhe (es. 111111111111111111111 contiene 11111111111) """
                first = re.sub(str(i)*10 + '1', defs[i]+r"\\textsubscript{g}", first)
                first = re.sub(str(i)*10 + '0', defs[i].lower()+r"\\textsubscript{g}", first)

            with open(str(current_path)+"/"+file, 'w', encoding='utf-8') as f:
                f.write(first)

def ReadAllWords(glox_path,defs:list):
    with open(glox_path,'r') as f:
        for line in f:
            if "\\subsection" in line:
                g_def = line.strip()[12:-1]
                defs.append(g_def)

def IsRecent(doc:str):
    date=doc.split('-')
    date[0] = date[0].split('_')[1]

    lower_bound = datetime.datetime(2024,11,13)
    document_date=datetime.datetime(int(date[0]),int(date[1]),int(date[2])) # date[0] = year, date[1] = month, date[2] = day
    return lower_bound<=document_date


if __name__ == "__main__":
    main()

