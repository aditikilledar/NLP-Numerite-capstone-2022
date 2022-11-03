'''main.py ensures calling of all modules in the order designed by our pipeline'''


class AMWPS:
    def __init__(self, mwp):
        self.mwp = mwp

    def identify_operation(self):
        op =