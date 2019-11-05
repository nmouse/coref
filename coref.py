import argparse
import math
from collections import deque
import re


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('list_file', action="store")
    parser.add_argument('response_dir', action="store")
    args = parser.parse_args()
    list_file = open(args.list_file, 'r')
    response_dir = str(args.response_dir)
    # list_file = open("lf-a9.txt", 'r')
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
    corefs = {}
    corefbase=[]
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
        for j in r:
            corefbase.append(j)
            line = line.replace(j,'')
        linelist = line.split()
        for word in linelist:
            WordDict[linen].append(word)
        linen=linen+1

    # acutal coreference finding logic
    for word in corefs:
        for key in WordDict:
            for element in WordDict[key]:
                # if the wordDict `word` contains `element` within as a substring
                # or if `element` contains `word` within as a substring and `word` < 3x as big as `element`
                if word.casefold() in element.casefold()\
                        or (element.casefold() in word.casefold() and len(word)/len(element) < 3):
                    corefs[word].append((element, key))

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

if __name__ == '__main__':
    main()