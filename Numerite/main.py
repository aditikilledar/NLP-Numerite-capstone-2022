'''main.py ensures calling of all modules in the order designed by our pipeline'''
import OperatorPrediction as opred


class AMWPS:
        def __init__(self, mwp):
                self.mwp = mwp
                self.operator = None;

        def identify_operation(self):
                self.operator = opred.predict_operation(self.mwp)

if __name__ == '__main__':
        inputmwp = 'In the fridge, there are 4 stacks of chocolate puddings and 5 stacks of pasta salad. How many stacks of dessert are there?'
        test_mwp = AMWPS(inputmwp)

        test_mwp.identify_operation()
        print(test_mwp.operator)