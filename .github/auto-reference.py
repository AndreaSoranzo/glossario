import pathlib as path
import os
import concurrent.futures
import datetime 
import re

DOCS_PATH = "Docs"
G_KEYWORD = "\\textsuperscript{g}"

def main(UseThread:bool=False):
    glox_path = path.Path(DOCS_PATH+"/Generali/glossario/01_intro.tex")

    defs = ReadAllWords(glox_path)

    if UseThread:
        with concurrent.futures.ThreadPoolExecutor(3) as pool: # with -> automatically wait for all threads
            for type in os.listdir(path.Path(DOCS_PATH)):
                if type == "Candidatura": # skippa la candidatura
                    continue
                pool.submit(Apply_g,defs,type)
    else:
        ApplyAll(defs)
        print(defs)


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
            with open(str(current_path)+"/"+file,'r+',encoding='utf-8') as f:
                lines = f.readlines()
                text = '$$'.join(lines)
                lines = f.readlines()
                for i,line in enumerate(lines): # for each line
                    current_line = line.split()
                    for word in current_line:   #for each word
                        isItalicOrBold = "\\textbf" in word or "\\textit" in word
                        if isItalicOrBold: # if it is \textbf or \textbf is a valid word anyway
                                word = word[8:-1]
                        if word.lower() in defs: # if word is in the definitions add pedice
                            line = line.replace(word,word+"\\textsuperscript{g}")
                            lines[i] = line
                f.seek(0)
                f.writelines(lines)

def ReadAllWords(glox_path):
    defs = []
    with open(glox_path,'r',encoding='utf-8') as f:
        for line in f:
            if "\\subsection" in line:
                g_def = line.strip()[12:-1]
                defs.append(g_def.lower())
    defs = sorted(defs, key=len,reverse=True)
    return defs

def IsRecent(doc:str):
    date=doc.split('-')
    date[0] = date[0].split('_')[1]

    lower_bound = datetime.datetime(2024,11,13)
    document_date=datetime.datetime(int(date[0]),int(date[1]),int(date[2])) # date[0] = year, date[1] = month, date[2] = day
    return lower_bound<=document_date


if __name__ == "__main__":
    main()

