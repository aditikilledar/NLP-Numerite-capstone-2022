import nltk
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