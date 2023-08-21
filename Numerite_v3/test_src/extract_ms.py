import nltk
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
import pandas as pd
import spacy
import benepar
import neuralcoref
import util
import re
from nltk.tokenize import sent_tokenize
import QuestionIdentification as quesid


class MicroStatements:
    """
    return microstatemnts from input mwp
    coref resolved and conjunction resolved.
    """
    def __init__(self, inputmwp):
        """
        initialising the neuralcoref pipeline
        """
        self.nlp_pronoun = spacy.load('en_core_web_sm')
        neuralcoref.add_to_pipe(self.nlp_pronoun, greedyness=0.52)
        #benepar.download('benepar_en3')
        self.nlp = spacy.load('en_core_web_sm')
        if spacy.__version__.startswith('2'):
            self.nlp.add_pipe(benepar.BeneparComponent("benepar_en3"))
        else:
            self.nlp.add_pipe("benepar", config={"model": "benepar_en3"})

        self.mwp = inputmwp
        self.corefmwp = None
    
    def clean_mwp(self):
        """
		spelling checker
		converts to Lowercase
		changes number names to numbers
		"""
        mwp = self.mwp.lower()
        mwp = util.spelling_correction(mwp)
        mwp = util.convertNumberNames(mwp)
        mwp = util.appendQuantities(mwp)
        #print(mwp)
        self.mwp = mwp
    
    def resolve_coref(self, sentence):
        """ 
		Neural coref resolution function
		@input : sentence without coref resolution
		@output : coref resolved sentence 
		"""
        doc = self.nlp_pronoun(sentence)
        #self.mwp = doc._.coref_resolved
        return doc._.coref_resolved

    def extract_microstatements(self, sentence):
        """
        @input : one sentence at a time without coref resolution, because coref resolution ruins the question
        @output : {set of microstatements from a single sentence input}

        Performed using Parsing a dependency tree generated by benepar (berkeley neural parser)
        """
        # convert all to lower case, because the logic runs on the assumption that the labels are upper case and everything else is lower
        sentence = sentence.lower()
        parts = " "
        doc = self.nlp(sentence)
        try:
            #print(list(doc.sents))
            sent = list(doc.sents)[0]
        except:
            return []
        dependency_tree = sent._.parse_string
        #print(dependency_tree)
        dependency_tree = dependency_tree.replace("(", "( ")
        dependency_tree = dependency_tree.replace(")", " )")
        dependency_tree = dependency_tree.split()
        #splitting dependency tree such that each label, bracket, word is a separate elememt in the list
        i =0
        sentence_splits= [] #split sentences on the basis of presence of conjuction
        flag_complex_sentence = False #save time if the sentence is simple
        while i<len(dependency_tree):
            if dependency_tree[i] == "CC" or (dependency_tree[i] == "," and dependency_tree[i+1] == ','):
                flag_complex_sentence = True
                if parts != "":
                    sentence_splits.append(parts) #if a conjuction is encountered, a new part is added to the sentence
                parts= ""
                while(dependency_tree[i] != ")"):
                    i+=1
            elif dependency_tree[i].islower() or dependency_tree[i].isnumeric():
                parts = parts + dependency_tree[i] + " "
                i=i+1
            else:
                i+=1
        sentence_splits.append(parts)
        #print(sentence_splits)
        if flag_complex_sentence == False:
            return [sentence]
        phrase_checker= [] #to check whether a phrase can be an independent sentence
        #extract_noun = []
        flag_no_verb = False
        for i in sentence_splits:
            #creates a dependency tree for each part of the sentence
            doc = self.nlp(i)
            sent = list(doc.sents)[0]
            #print(sent)
            dependency_tree = sent._.parse_string
            dependency_tree = dependency_tree.replace("(", "( ")
            dependency_tree = dependency_tree.replace(")", " )")
            dependency_tree = dependency_tree.split()
            #print(dependency_tree)
            #if a verb is present in the phrase then it is an independent sentence
            if "VP" in dependency_tree:
                phrase_checker.append([True,i,dependency_tree])
                #flag_no_verb = False 
            else:
                phrase_checker.append([False,i])
                #print(i, dependency_tree)
                flag_no_verb = True
                break
            #tells us if even one phrase is incomplete/dependent

            # if "JJ" in dependency_tree:
            #     last_adj_idx = max(idx for idx, val in enumerate(dependency_tree) if val == 'JJ')
            #     j = last_adj_idx
            #     flag_adj = False
            #     while(j<len(dependency_tree)):
            #         if dependency_tree[j] == "NN" or dependency_tree[j] == "NNS" or dependency_tree[j] == "NNP" or dependency_tree[j] == "NNPS":
            #             extract_noun.append([i, dependency_tree[j+1]])
            #             flag_adj = True
            #         j+=1
            #     if flag_adj == False:
            #         extract_noun.append([i, ""])
        
                    

        #print(extract_noun)
        if flag_no_verb:
            #print("never here")
            common_phrases_ls = []
            #to find a common phrase that will complete an incomplete phrase
            for i in phrase_checker:
                if i[0]:
                    #print(i[1])
                    common_phrase = ""
                    last_verb_idx = max(idx for idx, val in enumerate(i[2]) if val == 'VP') #finds the last verb in an independent sentence, copies the sentence up until then
                    for j in i[2][:last_verb_idx]:
                        if j.islower() or j.isnumeric():
                            common_phrase = common_phrase + j + " " #
                    last_verb_idx +=2
                    brackets = 1
                    while brackets>0: #to include the final verb in the sentence
                        if i[2][last_verb_idx] == "(":
                            brackets+=1
                        elif i[2][last_verb_idx] == ")":
                            brackets-=1
                        elif i[2][last_verb_idx].islower() or i[2][last_verb_idx].isnumeric():
                            common_phrase = common_phrase + i[2][last_verb_idx] + " "
                        else:
                            pass
                        last_verb_idx+=1
                    common_phrases_ls.append(common_phrase)
            true_count = 0 #checks which common phrase is applicable to which incomplete phrase
            for i in phrase_checker: 
                if i[0]:
                    true_count+=1 
                if not i[0]: #for all phrases that are dependent, it adds the common phrase to the start of the phrase
                    try:
                        i[1] = common_phrases_ls[true_count-1] +" "+ i[1]
                    except:
                        i[1] = i[1]

        micros = []
        #appends all the found phrases to the list of microstatements
        for i in phrase_checker:
            micros.append(i[1])
        #print(micros)
        '''in case of a noun that proceeds an adjective, the noun does not get included into the microstatement.
        This is to append that extra noun in all sentences where it remains missing'''
        #print(micros)
        extract_noun = []
        for i in micros:
           # print(i)
            doc = self.nlp(i)
            sent = list(doc.sents)[0]
            dependency_tree = sent._.parse_string
            dependency_tree = dependency_tree.replace("(", "( ")
            dependency_tree = dependency_tree.replace(")", " )")
            dependency_tree = dependency_tree.split()
            #print(dependency_tree)
            if "JJ" in dependency_tree:
                #print(dependency_tree) #checks to see if this is a concern for us at all
                last_adj_idx = max(idx for idx, val in enumerate(dependency_tree) if val == 'JJ')
                j = last_adj_idx #finds the last adjective in the sentence
                #print(j)
                flag_adj = False
                temp_noun = ""
                while(j<len(dependency_tree)): #checks to see if there is a noun after the adjective
                    if dependency_tree[j] == "NN" or dependency_tree[j] == "NNS" or dependency_tree[j] == "NNP" or dependency_tree[j] == "NNPS":
                        temp_noun = temp_noun + dependency_tree[j+1] + " "
                        flag_adj = True
                    j+=1
                extract_noun.append([i,temp_noun])   
                
                if flag_adj == False:
                    extract_noun.append([i, ""]) #if there is no noun after the adjective, then the noun is missing and needs to be added
            else:
                extract_noun.append([i,"ignore"]) #if there is no adjective, then we don't need to worry about this sentence
        modified_micros = []
        #print(extract_noun)
        for i in range(len(extract_noun)):
            #print("extract_nouns", extract_noun[i])
            if extract_noun[i][1] !="": #if the noun is not empty, then we add it to the microstatements list, since it is a complete sentence
                #print("i was here")
                modified_micros.append(extract_noun[i][0])
            else:
                #print("i came here")
                temp = i+1
                while(temp<len(extract_noun)):
                    if extract_noun[temp][1] =="ignore": #sentences that don't have an adjective are ignored
                        temp+=1
                        continue
                    elif extract_noun[temp][1]=="": #if the next sentence also doesn't have a noun, then we ignore it
                        temp+=1
                        continue
                    else: #if the sentence has a noun, we extract that and add it to the current microstatement
                        temp_micro = extract_noun[i][0] + " " + extract_noun[temp][1]
                        modified_micros.append(temp_micro)
                        break
                    temp+=1
        return modified_micros

    def get_microstatements(self):
        micros = []
        self.clean_mwp()
        #self.resolve_coref()
        for sent in self.mwp.split('.'):
            micros.extend(self.extract_microstatements(sent))
            # print('For sentence:\n', sent, '\nMS:\n', micros)
        final_micros = []
        for i in micros:
            i = re.sub(r'[^\w\s]', '', i)
            final_micros.append(i)
        quesornot = quesid.identify_question(final_micros)
        #print(quesornot)
        body_string = ""
        for i in quesornot['statements']:
            body_string = body_string + i + "."
        print('---------before neuralcoref------------------')
        body_string = self.resolve_coref(body_string)
        final_micros = body_string[:-1].split(".")
        final_micros.append(quesornot['question'][0])
        #print(final_micros)
        return final_micros

if __name__ == '__main__':
    
    # inputmwp1 = "She bought 5 apples"
    # inputmwp2 = "If there are 2 boxes, how many pens are there in total?"
    # inputmwp3 = "She and I went to the supermarket"
    # inputmwp4 = "She drank wine and i ate fish"
    # inputmwp5 = "Joel bought 2 oranges and 4 apples and Angela bought 3 peaches and 2 oranges. "
    # inputmwp6 = "ashley bought 5 apples and joel ate 3 oranges."
    # inputmwp7 = "Joel bought 2 ornges and three apples. Angle bought three peaches and 2 oranges. How many oranges does Joel have?"

    # mainmwp1 = 'Rahul has 4 cats. He gets three more cats. How many cats does he have now?'
    # mainmwp2 = 'There are 9 boxes and 2 pencils in each box. How many pencils are there altogether?'
    mwp = "joe has five and amy has 6 apples. how many apples do they have in total?"
    ms = MicroStatements(mwp)
    print(ms.get_microstatements())