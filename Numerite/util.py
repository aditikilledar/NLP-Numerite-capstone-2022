import nltk
import jamspell
import re
from word2number import w2n

def spelling_correction(mwp):
    corrector = jamspell.TSpellCorrector()
    corrector.LoadLangModel('./models/en.bin')
    return corrector.FixFragment(mwp)

def convertNumberNames(sentence):
    lstr = re.findall( r'\w+|[^\s\w]+', sentence)
    res = []
    i = 0
    status = []
    # False if word isnt a number indicated by exception
    for i in range(len(lstr)):
        try:
            w2n.word_to_num(lstr[i])
            status.append(True)
        except:
            # for complex number names like "one hundred and thirty five"
            if lstr[i]=='and' and i>0 and status[i-1] == True:
                status.append(True)
            else:
                status.append(False)
    j = 0
    # convert all the consecutive True's to a number eg. ten -> 10; thirty, five -> 35
    final_ls = []
    while j<len(lstr):
        quant = ""
        while(status[j]==True):
            quant = quant+lstr[j]+" "
            j=j+1
        if quant!="":
            final_ls.extend([str(w2n.word_to_num(quant)),lstr[j]])
        else:
            final_ls.append(lstr[j])
        j=j+1
    final_ls = " ".join(final_ls)
    return final_ls

def extractAll(txt):
    wordsList = nltk.word_tokenize(txt)
    #wordsList = [w for w in wordsList if not w in stop_words]
    
    tagged = nltk.pos_tag(wordsList)
    # determining the units in the word problem 
    
    unit = [""]
    for i in range(len(tagged)-2):
        if tagged[i][1] == "CD":
            if tagged[i+1][1] == "NN" or tagged[i+1][1]=='NNP'  or  tagged[i+1][1]=='NNS' or tagged[i+1][1]=='NNPS' :
                unit.append(tagged[i+1])
            elif tagged[i+2][1]=='NN' or tagged[i+2][1]=='NNP' or tagged[i+2][1]=='NNS' or tagged[i+2=='NNPS']:
                unit.append(tagged[i+2])

    #appending units 
    for i in range(len(tagged)):
        if (tagged[i][1] == 'CD'):
            if(tagged[i+1][1]!='NN' and tagged[i+1][1]!='NNS'):
                tagged.insert(i+1,unit[1])

    entities = list()
    s =""
    #extracting quantities
    for i in range(len(tagged)-2):
        if tagged[i][1] == "CD":
            if tagged[i+1][1] == "NN" or tagged[i+1][1]=='NNP'or tagged[i+1][1]=='NNPS' or tagged[i+2][1]=='NN' or tagged[i+2][1]=='NNP'or tagged[i+2][1]=='NNPS' or  tagged[i+1][1]=='NNS' or tagged[i+2][1]=='NNS' :
                s = tagged[i][0] + " "+ tagged[i+1][0]
                entities.append(s)
    
    return(entities)

sp = spelling_correction('Sam has one hudred and three aples')
print(sp)
print(convertNumberNames(sp))
