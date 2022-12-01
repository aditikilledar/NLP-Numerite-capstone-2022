'''main.py ensures calling of all modules in the order designed by our pipeline'''
#import OperatorPrediction as opred
import nltk
import spacy
from extract_ms import MicroStatements
from deepmultilingualpunctuation import PunctuationModel
import IIRU as iiru
import pandas as pd
import jamspell
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
    
    # def identify_operation(self):
    #     # predicts and stores operation of the mwp
    #     self.operation = opred.predict_operation(self.mwp)
    #     # print('\nOperation: ', self.operation)
    
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
            ops.append(num)
        
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
        result = eval(self.equation)
        self.solution = result

    def explain_eqn(self):
            """ generates explanation """
            newline = '\n'
            # expression = f"{op1} {self.operator} {self.op2}"
            expression = self.equation
            # result = int(eval(expression))
            anstr = f"Operation: {self.operation}{newline}Equation: {expression}{newline}Explanation:{newline}The unknown 'x', can be found using the equation:{newline}x = {self.op1} {self.operator} {self.op2}{newline}Which is then simplified using the {self.operation} operator to get:{newline}x = {self.solution}" 
            self.explanation = anstr

    def solve(self, operation):
        # self.identify_operation()
        self.operation = operation
        self.get_microstatements()
        self.remove_irrelevant()                 
        self.make_equation()          
        self.solve_equation()
        self.explain_eqn()  
        #return self.operation
        return self.solution

if __name__ == '__main__':
        # inputmwp = 'There are 9 boxes. There are 2 pencils in each box. How many pencils are there altogether?'
        #inputmwp = 'Virginia has 16 eggs and 8 Skittles. If she shares the eggs among 4 friends, how many eggs does each friend get?'
        #inputmwp = 'Rahul has 4 cats. He gets 3 more cats and 50 dogs. How many cats does he have now?'
        model = PunctuationModel()
        corrector = jamspell.TSpellCorrector()
        corrector.LoadLangModel('./models/en.bin.spell')
        df = pd.read_json('../data/Singleop/singleopadd.json')

        op = open("Results/SingleOp/Just_Operator/Op_output_add.txt", "r")
        predicted = [line[:len(line)-1] for line in op if line[0].islower()]
        op.close()
        #print(predicted)
        questions = df['sQuestion'].tolist()
        answers = df['lSolutions'].tolist()
        print(questions[0], answers[0][0])
        # test_mwp = AMWPS(questions[0])
        # ans = test_mwp.solve()
        # print(ans)
        #f = open("add_sop_res.txt", "a")
        total_q = len(questions)
        # # f.write("Total questions: " + str(total_q))
        print(total_q)
        correct_pred = 0
        skipped_questions = []
        count_skip = 0
        wrong_ans = []
        for i in range(total_q):
            print(questions[i])
            #try:
            mwp = model.restore_punctuation(questions[i])
            mwp = corrector.FixFragment(mwp)
            test_mwp = AMWPS(mwp)
            test_mwp.solve(predicted[i])
            ans = test_mwp.solution
            print(ans)
            print(answers[i][0])
            if ans == answers[i][0]:
                correct_pred+=1
            else:
                wrong_ans.append(questions[i])
            # except:
            #     skipped_questions.append(questions[i])
            #     count_skip+=1
            #     print("Skipped: ", count_skip)
            print(correct_pred)
            #f.write("\nTotal predictions: " + str(i))
            #f.write("\nCorrect predictions: " + str(correct_pred))
            print("Accuracy: ", (correct_pred/total_q))
            #print("Accuracy after removing skipped questions: ",correct_pred/calc_q )
        
        #f.write("\nAccuracy: " + str(correct_pred/total_q))
        calc_q = total_q- count_skip
        #f.write("\nAccuracy after removing skipped questions: " +str(correct_pred/calc_q))
        #f.close()
        with open(r'wrong_ques_add.txt', 'w') as fp:
            for item in wrong_ans:
                # write each item on a new line
                fp.write("%s\n" % item)
        # print("Accuracy: ", (correct_pred/total_q))
        # print("Accuracy after removing skipped questions: ",correct_pred/calc_q )
        
        # test_mwp = AMWPS(inputmwp)
        # test_mwp.solve()
        
        # print(test_mwp.operation)
        # print(test_mwp.microstatements)
        # print(test_mwp.kb)

        # uncomment next 2 lines if you get eqn with None in it
        # print(test_mwp.equation)
        # print(test_mwp.solution)
        # print(test_mwp.explanation)