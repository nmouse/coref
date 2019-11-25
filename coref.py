import argparse
import math
import spacy
from collections import deque
import re


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('list_file', action="store")
    parser.add_argument('response_dir', action="store")
    args = parser.parse_args()
    list_file = open(args.list_file, 'r')
    response_dir = str(args.response_dir)
    # list_file = open("lf-b1.txt", 'r')
    # response_dir = "./OUTPUT.txt"
    inputs = list_file.readlines()
    simulate(inputs, response_dir)


def simulate (inputs, output_file):
    files = []
    for line in inputs:
        line = line.rstrip('\n')
        inputfilew = open(line, 'r')
        files.append(inputfilew)
    for run in files:
        run_split = str(run).split('/')
        output_file_path = output_file + run_split[len(run_split)-1].split('.')[0] + ".response"
        coref(run, output_file_path)
        # coref(run, output_file)
    return


def coref(run, output):
    WordDict = {}
    spacyWordDict = {} #-----------spacy
    corefs = {}
    spacycorefs = {} #-----------spacy
    corefbase = []
    nlp = spacy.load("en_core_web_sm") #-----------spacy
    linen = 0

    for line in run:
        WordDict[linen] = []
        linenumber = '<S ID="'+str(linen)+'">'
        line = line.replace(linenumber,'')
        line = line.replace('</S>','')
        line = line.replace(',','')
        c = re.findall(r'<COREF ID="X.*?">(.*?)</COREF>', line)
        r = re.findall(r'<COREF ID="X.*?">.*?</COREF>', line)
        for i in c:
            corefs[i]=[]
            spacycorefs[i]= nlp(i) #-----------spacy
        for j in r:
            corefbase.append(j)
            line = line.replace(j,'')
        linelist = line.split()

        doc = nlp(line) # -------------spacy

        # print("(" + str(linen) + ") " + line, end="")
        # print("noun_chunks --> ", end="")
        # noun_phrases = list(doc.noun_chunks)
        # for np in noun_phrases:
        #     print("[" + np.text + "] ", end="")
        # print()
        # print("ents ---------> ", end="")
        # ents = list(doc.ents)
        # for ent in ents:
        #     print("[" + ent.label_ + ": " + ent.text + "] ", end="")
        # print("\n")

        for word in linelist:
            WordDict[linen].append(word)
        spacyWordDict[linen] = doc #-----------spacy
        linen = linen+1

    # coreference finding logic
    for coref in corefs:
        corefdoc = nlp(coref)
        # SPACY
        for key in spacyWordDict:
            match = False
            # NOUN PHRASE MATCHING
            for np in list(spacyWordDict[key].noun_chunks):
                # HEAD NOUN
                tokens = list(np)
                np_start_noun = tokens[0]
                np_end_noun = tokens[len(tokens)-1]
                if np_end_noun.text.casefold() in coref.casefold() and len(coref) / len(np_end_noun.text) < 2.5:
                    corefs[coref].append((np_end_noun.text, key))
                    match = True
                elif np_start_noun.text.casefold() in coref.casefold() and len(coref) / len(np_start_noun.text) < 1.3:
                    corefs[coref].append((np_start_noun.text, key))
                    match = True
                if not match:
                    # EDIT DISTANCE STRING MATCHING
                    if len(coref) <= len(np.text):
                        if coref.casefold() in np.text.casefold()\
                        and editDist(coref.casefold(), np.text.casefold(), len(coref), len(np.text)) < 1:
                            corefs[coref].append((np.text, key))
                            match = True
                    else:
                        if np.text.casefold() in coref.casefold() \
                        and editDist(coref.casefold(), np.text.casefold(), len(coref), len(np.text)) < 5:
                            corefs[coref].append((np.text, key))
                            match = True
            # ENTITY MATCHING
            for ent in list(spacyWordDict[key].ents):
                if (ent.text.casefold() in coref.casefold() and not match):
                    corefs[coref].append((ent.text, key))
                    match = True

    i = 0
    outputfile= open(output, 'w')
    for word, base in zip(corefs,corefbase):
        outputfile.write(base+'\n')
        for pairs in corefs[word]:
            outputs = '{'+str(pairs[1])+'} {'+str(pairs[0])+'}\n'
            outputfile.write(outputs)
        if (i != len(corefs)-1):
            outputfile.write('\n')
        i += 1
    outputfile.close()
    return


# Used from https://www.geeksforgeeks.org/edit-distance-dp-5/
def editDist(str1, str2, m, n):
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i][j - 1],  # Insert
                                   dp[i - 1][j],  # Remove
                                   dp[i - 1][j - 1])  # Replace
    return dp[m][n]


if __name__ == '__main__':
    main()