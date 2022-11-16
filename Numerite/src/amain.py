'''main.py ensures calling of all modules in the order designed by our pipeline'''
import OperatorPrediction as opred
import nltk
import spacy
from Microstatements import MicroStatements as microstats
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
        # inputmwp = 'There are 9 boxes. There are 2 pencils in each box. How many pencils are there altogether?'
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