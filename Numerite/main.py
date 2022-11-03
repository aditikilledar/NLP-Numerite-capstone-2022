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