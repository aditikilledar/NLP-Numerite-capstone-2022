'''main.py ensures calling of all modules in the order designed by our pipeline'''
import OperatorPrediction as opred
import nltk
import spacy
from extract_ms import MicroStatements
from util import extractAll
import IIRU as iiru

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
        # predicts and stores operation of the mwp
        self.operation = opred.predict_operation(self.mwp)
    
    def get_microstatements(self):
        # parses and gets microstatements of the mwp
        ms = MicroStatements()
        self.microstatements = ms.get_microstatements(self.mwp)

    def remove_irrelevant(self):
        # gets all the knowledge from KB that is relevant to the question at hand
        # removes all the irrelevant info from the KB
        relevantKB = iiru.IIRU(self.microstatements, self.operation)

    def make_equation(self):
        """ makes the equation using the quantities known, and the operation 
            stores in self.equation, and inits vals to self.op1 and self.op2
        """
        # TODO
        pass

    def solve_equation(self):
        """ solves self.equation and stores the solution in self.solution """
        # TODO
        pass

    def explain_eqn(self):
            """ generates explanation """
            newline = '\n'
            expression = f"{self.op1} {self.operator} {self.op2}"
            # result = int(eval(expression))
            anstr = f"Equation: {expression}{newline}Explanation:{newline}The unknown, can be calculated using the equation:{newline}x = {self.op1} {self.operator} {self.op2}{newline}Which is then simplified using the {self.operation} operator to get:{newline}x = {self.solution}" 
            self.explanation = anstr

    def solve(self):
        self.identify_operation()
        self.get_microstatements()
        self.remove_irrelevant()                 
        self.make_equation()          
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