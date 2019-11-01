import argparse
import math
from collections import deque
import re


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', action="store")
    parser.add_argument('output', action="store")
    args = parser.parse_args()
    inputfile = open(args.input, 'r')
    inputs = inputfile.readlines()
    outputsfile = open(args.output, 'w+')
    simulate(inputs,outputsfile)



def simulate(inputs,outputfile):
    files = []
    for line in inputs:
        line = line.rstrip('\n')
        inputfilew=open(line, 'r')
        files.append(inputfilew)
    for run in files:
        coref(run,outputfile)

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
    for word in corefs:
        for key in WordDict:
            for element in WordDict[key]:
                if element.casefold()==word.casefold():
                    corefs[word].append((word,key))
    
if __name__ == '__main__':
    main()