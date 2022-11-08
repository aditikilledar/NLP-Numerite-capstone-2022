'''main.py ensures calling of all modules in the order designed by our pipeline'''
import OperatorPrediction as opred
import nltk
import spacy
from Microstatements import MicroStatments as microstats

class AMWPS:
        def __init__(self, mwp):
                self.mwp = mwp
                self.operator = None;
                self.microstatements = []
                self.solution = None
                self.kb = []
                self.equation = ''
        
        def identify_operation(self):
                self.operator = opred.predict_operation(self.mwp)
        
        def get_microstatements(self):
            ms = microstats()
            self.microstatements = ms.mwp_split(self.mwp)
        
        def KB(self):
            ner = spacy.load("en_core_web_sm")
            res = []
            for statement in self.microstatements: # ignore question microstatement
                parsed = ner(statement)
                owner = ''
                quantity = ''
                obj = ''
                
                for word in parsed.ents:
                #print(word.label_, word.text, i)
                    if word.label_ == "CARDINAL":
                        quantity = word.text
                    elif word.label_ == "PERSON" or word.label == "ORG":
                        owner = word.text
                    
                    words = nltk.word_tokenize(statement)
                    for i, w in enumerate(words):
                        if w.isnumeric():
                            obj = words[i + 1]

                    res.append((obj, owner, quantity))
            
            self.kb = res

        def get_equation(self):
            # TODO
            pass
        
        def solve_equation(self):
            # TODO
            pass
        
        def solve(self):
            self.get_microstatements()
            self.identify_operation()
            # self.KB()                 TODO
            # self.get_equation()       TODO   
            # self.solve_equation()     TODO

            return self.solution

if __name__ == '__main__':
        inputmwp = 'there are 9 boxes. there are 2 pencils in each box. how many pencils are there altogether?'
        test_mwp = AMWPS(inputmwp)

        test_mwp.identify_operation()
        test_mwp.get_microstatements()
        print(test_mwp.operator)
        print(test_mwp.microstatements)
        
        # test_mwp.solve(inputmwp)