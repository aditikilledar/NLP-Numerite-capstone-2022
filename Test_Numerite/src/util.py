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
    # print(lstr)
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
                if i<len(lstr)-1:
                    try:
                        w2n.word_to_num(lstr[i+1])
                        status.append(True)
                    except:
                        status.append(False)
                else:
                    status.append(False)
            else:
                status.append(False)
    
    j = 0
    # print(status)
    # convert all the consecutive True's to a number eg. ten -> 10; thirty, five -> 35
    final_ls = []
    while j<len(lstr):
        quant = ""
        while(status[j]==True):
            quant = quant+lstr[j]+" "
            j=j+1
        if quant!="":
            try:
                final_ls.extend([str(w2n.word_to_num(quant)),lstr[j]])
            except:
                final_ls.extend([quant.strip(),lstr[j]])
        else:
            final_ls.append(lstr[j])
        j=j+1
    final_ls = " ".join(final_ls)
    return final_ls

def appendQuantities(txt):
    wordsList = nltk.word_tokenize(txt)
    #wordsList = [w for w in wordsList if not w in stop_words]
    
    tagged = nltk.pos_tag(wordsList)
    # determining the units in the word problem 
    
    unit = []
    for i in range(len(tagged)-2):
        #print(tagged[i])
        if tagged[i][1] == "CD":
            #print(tagged[i], "Here")
            j = i+1
            while(j<len(tagged)-1):
                #print(tagged[j])
                if (tagged[j][1]=="NN" or tagged[j][1]=="NNS"):
                    #print(tagged[i][0],"HERE")
                    unit.append([tagged[j][0], j])
                    #print("Unit", unit)
                    break
                else:
                    j=j+1
                    break
    #appending units
    #print(unit) 
    unit_count = 0
    new_mwp = ""
    for i in range(len(tagged)):
        if unit_count<len(unit)-1 and unit[unit_count][1] == i :
            unit_count+=1
        if (tagged[i][1] == 'CD' and tagged[i+1][1]!='NN' and tagged[i+1][1]!='NNS') and unit != []:
                #tagged.insert(i+1,unit[unit_count])
                new_mwp = new_mwp + tagged[i][0] + " " + unit[unit_count][0] + " "
        else:
            new_mwp = new_mwp + tagged[i][0] + " "
    
    return new_mwp

    # entities = list()
    # s =""
    # #extracting quantities
    # for i in range(len(tagged)-2):
    #     if tagged[i][1] == "CD":
    #         #if tagged[i+1][1] == "NN" or tagged[i+1][1]=='NNP'or tagged[i+1][1]=='NNPS' or tagged[i+2][1]=='NN' or tagged[i+2][1]=='NNP'or tagged[i+2][1]=='NNPS' or  tagged[i+1][1]=='NNS' or tagged[i+2][1]=='NNS' :
    #         if tagged[i+1][1] == "NN" or tagged[i+2][1]=='NN' or tagged[i+1][1]=='NNS' or tagged[i+2][1]=='NNS' :
    #             s = tagged[i][0] + " "+ tagged[i+1][0]
    #             entities.append(s)
    
    # return(entities)
#print(convertNumberNames("Joe has five and amy has 6 apples"))
