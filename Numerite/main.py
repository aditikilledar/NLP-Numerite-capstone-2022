'''main.py ensures calling of all modules in the order designed by our pipeline'''
import OperatorPrediction as opred
from Microstatements import MicroStatments as microstats

class AMWPS:
        def __init__(self, mwp):
                self.mwp = mwp
                self.operator = None;
                self.microstatements = []
        def identify_operation(self):
                self.operator = opred.predict_operation(self.mwp)
        def get_microstatements(self):
            ms = microstats()
            self.microstatements = ms.mwp_split(self.mwp)

if __name__ == '__main__':
        inputmwp = 'There are 9 boxes. There are 2 pencils in each box. How many pencils are there altogether?'
        test_mwp = AMWPS(inputmwp)

        test_mwp.identify_operation()
        test_mwp.get_microstatements()
        print(test_mwp.operator)
        print(test_mwp.microstatements)