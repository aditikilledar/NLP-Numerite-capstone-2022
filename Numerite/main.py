'''main.py ensures calling of all modules in the order designed by our pipeline'''
import OperatorPrediction as opred
import nltk
import spacy
from Microstatements import MicroStatments as microstats
from util import extractAll

class AMWPS:
    def __init__(self, mwp):
        self.mwp = mwp
        self.operation = None
        self.operator = None
        self.microstatements = []
        self.solution = None
        self.kb = []
        self.quantities = []
        self.equation = ''
        self.op1 = None
        self.op2 = None
    
    def identify_operation(self):
        self.operation = opred.predict_operation(self.mwp)
    
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

        if self.operation is None:
            self.identify_operation()
        operation = self.operation
        opnames = {'addition': '+', 'subtraction': '-', 'multiplication': '*', 'division': '/'}
        operator = opnames[operation]
        self.operator = operator

        if len(quantities) == 2:    
            self.op1 = quantities[0]
            self.op2 = quantities[1]
            self.equation = f"{self.op1} {self.operator} {self.op2}"
        else:
            # ideally there should be exactly two quantities, but this should handle edge cases
            # equation = ''
            for quant in quantities:
                self.equation = self.equation+quant+operator
            self.equation = self.equation[:-1]
    
    def solve_equation(self):
        if self.operation == None:
            self.identify_operation()
        if self.quantities == []:
            self.get_equation()
        operation = self.operation
        quantities = self.quantities
        solution = int(quantities.pop(0))
        if operation == 'addition':
            while quantities:
                solution += int(quantities.pop(0))
        if operation == 'subtraction':
            while quantities:
                solution -= int(quantities.pop(0))
        if operation == 'division':
            while quantities:
                solution /= int(quantities.pop(0))
        if operation == 'multiplication':
            while quantities:
                solution *= int(quantities.pop(0))
        
        self.solution = solution
        return solution

    def explain_eqn(self):
            """ generates explanation """
            newline = '\n'
            expression = f"{self.op1} {self.operator} {self.op2}"
            # result = int(eval(expression))
            anstr = f"Equation: {expression}{newline}Explanation:{newline}The unknown, can be calculated using the equation:{newline}x = {self.op1} {self.operator} {self.op2}{newline}Which is then simplified using the {self.operation} operator to get:{newline}x = {self.solution}" 
            self.explanation = anstr

    def solve(self):
        self.get_microstatements()
        self.identify_operation()
        self.KB()                 
        self.get_equation()          
        self.solve_equation()
        self.explain_eqn()  
    
        return self.solution

if __name__ == '__main__':
        # inputmwp = 'there are 9 boxes. there are 2 pencils in each box. how many pencils are there altogether?'
        inputmwp = 'Rahul has 4 cats. He gets 3 more cats. How many cats does he have now?'
        test_mwp = AMWPS(inputmwp)
        test_mwp.solve()
        # print(test_mwp.operation)
        # print(test_mwp.microstatements)
        # print(test_mwp.kb)

        # uncomment next 2 lines if you get eqn with None in it
        # print(test_mwp.equation)
        # print(test_mwp.solution)
        
        print(test_mwp.explanation)