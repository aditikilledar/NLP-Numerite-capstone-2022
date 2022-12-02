'''main.py ensures calling of all modules in the order designed by our pipeline'''
import OperatorPrediction as opred
import nltk
import spacy
from extract_ms import MicroStatements
#from util import extractAll
import IIRU as iiru
import pandas as pd
from deepmultilingualpunctuation import PunctuationModel

class AMWPS:
    def __init__(self, mwp):
        self.mwp = mwp
        self.operation = None
        self.operator = None
        self.microstatements = []
        self.solution = None
        self.kb = None
        self.cardinals = None
        self.equation = ''
        self.op1 = None
        self.op2 = None
    
    def identify_operation(self):
        # predicts and stores operation of the mwp
        self.operation = opred.predict_operation(self.mwp)
        # print('\nOperation: ', self.operation)
    
    def get_microstatements(self):
        # parses and gets microstatements of the mwp
        ms = MicroStatements(self.mwp)
        self.microstatements = ms.get_microstatements()
        # print('\nMicroStatements: ', self.microstatements)

    def remove_irrelevant(self):
        # gets all the knowledge from KB that is relevant to the question at hand
        # removes all the irrelevant info from the KB
        relevantKB, cardinalsKB = iiru.IIRU(self.microstatements, self.operation)
        self.kb = relevantKB
        self.cardinals = cardinalsKB
        # print('\n Relevant:\n', self.kb, '\n', self.cardinals)

    def make_equation(self):
        """ makes the equation using the quantities known, and the operation 
            stores in self.equation
        """
        # TODO 
        opnames = {'multiplication': '*', 'subtraction': '-', 'addition': '+', 'division': '/'}
        self.operator = opnames[self.operation]

        ops = []
        for _, num in self.cardinals.items():
            ops.extend(num)
        
        # assume two operands
        eqn = ''
        try:
            self.op1, self.op2 = ops[0], ops[1]
        except:
            self.op1, self.op2 = 0, -1
        if self.operation == 'division' or self.operation == 'subtraction':
            if self.op1 > self.op2:
                eqn = f"{self.op1} {self.operator} {self.op2}"
            else:
                eqn = f"{self.op2} {self.operator} {self.op1}"
        else:
            eqn = f"{self.op1} {self.operator} {self.op2}"

        self.equation = eqn


    def solve_equation(self):
        """ solves self.equation and stores the solution in self.solution """
        # TODO
        # type int to not show decimals in case of division
        result = int(eval(self.equation))
        self.solution = result

    def explain_eqn(self):
            """ generates explanation """
            newline = '\n'
            # expression = f"{op1} {self.operator} {self.op2}"
            expression = self.equation
            # result = int(eval(expression))
            anstr = f"Operation: {self.operation}{newline}Equation: {expression}{newline}Explanation:{newline}The unknown 'x', can be found using the equation:{newline}x = {self.op1} {self.operator} {self.op2}{newline}Which is then simplified using the {self.operation} operator to get:{newline}x = {self.solution}" 
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
        # addition
        #inputmwp ='Aditi has 37 blue balloons and Sandy has 28 green balloons. Sally has 39 blue balloons. How many blue balloons do they have in all?'

        # NEED ONE FOR SUBTRACTION
        #inputmwp = 'John has 36 cats. He gives away 12 cats to someone. How many cats does he have now?'


        # multiplication
        inputmwp = 'There are 9 boxes. There are 2 pencils in each box. How many pencils are there altogether?'
        # inputmwp = 'Rahul has 4 cats. He gets 3 more cats and 50 dogs. How many cats does he have now?'
        model = PunctuationModel()
        # division
        #inputmwp  = 'There are 10 oranges and the oranges are distributed among five children. How many oranges does each get?'
        #inputmwp = 'Peter has 16 eggs and 8 balloons. If he shares the eggs among 4 friends, how many eggs does each friend get?'
        # inputmwp = 'Virginia has 16 eggs and 8 Skittles. If she shares the eggs among 4 friends, how many eggs does each friend get?'
        # inputmwp = "Peter has 16 eggs, two blue and 8 red balloons. If he shares the eggs among 4 friends, how many eggs does each friend get?"
        inputmwp = 'Peter has sixteen eggs and 8 pencils. If he distributes the pencils among 4 people, how many pencils does each get?'
        # inputmwp = "Joe and Amy went shopping. Joe bought 4 and Amy bought 6 apples. How many apples did they buy altogether?"
        inputmwp = "If Harold split 15 apples between 3 people in her class and kept the left overs, how many apples did each classmate get?"
        inputmwp = model.restore_punctuation(inputmwp)
        test_mwp = AMWPS(inputmwp)
        test_mwp.solve()
        
        print(test_mwp.operation)
        print(test_mwp.microstatements)
        print(test_mwp.kb)

        # uncomment next 2 lines if you get eqn with None in it
        print(test_mwp.equation)
        print(test_mwp.solution)
        print(test_mwp.explanation)