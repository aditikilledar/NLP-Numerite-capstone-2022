<<<<<<< Updated upstream
'''main.py ensures calling of all modules in the order designed by our pipeline'''
import OperatorPrediction as opred


class AMWPS:
        def __init__(self, mwp):
                self.mwp = mwp
                self.operator = None;

        def identify_operation(self):
                self.operator = opred.predict_operation(self.mwp)

if __name__ == '__main__':
        inputmwp = 'There are 9 boxes. There are 2 pencils in each box. How many pencils are there altogether?'
        test_mwp = AMWPS(inputmwp)

        test_mwp.identify_operation()
        print(test_mwp.operator)
=======
'''main.py ensures calling of all modules in the order designed by our pipeline'''
import OperatorPrediction as opred
import nltk
import spacy
from Microstatements import MicroStatments as microstats
from util import extractAll

import benepar
benepar.download('benepar_en3')


class AMWPS:
    def __init__(self, mwp):
        self.mwp = mwp
        self.operator = None;
        self.microstatements = []
        self.solution = None
        self.kb = []
        self.quantities = []
        self.equation = ''
        self.op1 = None
        self.op2 = None
        self.explanation = None
    
    def identify_operation(self):
        self.operator = opred.predict_operation(self.mwp)
    
    def get_microstatements(self):
        ms = microstats()
        self.microstatements = ms.mwp_split(self.mwp)
    
    def KB(self):
        ner = spacy.load("en_core_web_sm")
        res = []
        
        if self.microstatements == []:
            self.get_microstatements()
        
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

    def __extract_quantities(self):
        if self.microstatements == []:
            self.get_microstatements()
        statements = '. '.join(self.microstatements)
        return extractAll(statements)

    def get_equation(self):
        quantities = self.__extract_quantities()
        quantities = [x.split(' ')[0] for x in quantities]
        self.quantities = quantities
        if self.operator is None:
            self.identify_operation()
        
        operation = self.operator
        equation =""
        # if operation=='Addition':
        #     operator = "+"
        # if operation=='Multiplication':
        #     operator = "*"
        # if operation=='Division':
        #     operator = "/"
        # if operation=='Subtraction':
        #     operator = "-"
        opnames = {'addition': '+', 'subtraction': '-', 'multiplication': '*', 'division': '/'}
        operator = opnames[operation]

        for i in quantities:
            equation = equation+i+operator
        self.equation = equation[:-1]

        return equation[:-1]
    
    def solve_equation(self):
        """ solves the generated equation """
        if self.operator == None:
            self.identify_operation()
        if self.quantities == []:
            self.get_equation()
        operation = self.operator
        quantities = self.quantities
        solution = int(quantities.pop(0))
        if operation == 'Addition':
            while quantities:
                solution += int(quantities.pop(0))
        if operation == 'Subtraction':
            while quantities:
                solution -= int(quantities.pop(0))
        if operation == 'Division':
            while quantities:
                solution /= int(quantities.pop(0))
        if operation == 'Multiplication':
            while quantities:
                solution *= int(quantities.pop(0))
        
        self.solution = solution
        return solution

    def explain_eqn(self):
        """ generates explanation """
        self.op1 = self.equation[1:]
        self.op2 = self.equation[-1:]
        newline = '\n'
        opnames = {'+': 'addition', '-': 'subtraction', '*': 'multiplication', '/':'division'}
        expression = f"{self.op1} {self.operator} {self.op2}"
        # result = int(eval(expression))
        anstr = f"The unknown, can be calculated using the equation:{newline}x = {self.op1} {self.operator} {self.op2}{newline}Which is then simplified using the properties of the {opnames[self.operator]} operator to get:{newline}x = {self.solution}" 
        self.explanation = anstr

    def solve(self):
        self.get_microstatements()
        self.identify_operation()
        self.KB()                 
        self.get_equation()          
        self.solve_equation()     
    
        return self.solution

if __name__ == '__main__':
    inputmwp = 'there are 9 boxes. there are 2 pencils in each box. how many pencils are there altogether?'
    test_mwp = AMWPS(inputmwp)
    test_mwp.solve()
    print(test_mwp.operator)
    print(test_mwp.microstatements)
    print(test_mwp.kb)
    print(test_mwp.equation)
    print(test_mwp.solution)
    print(test_mwp.explanation)
>>>>>>> Stashed changes
