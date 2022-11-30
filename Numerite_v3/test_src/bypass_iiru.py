import OperatorPrediction as opred
import nltk
import spacy
from extract_ms import MicroStatements
import pandas as pd
import QuestionIdentification as quesid
import inflect
#nltk.download('omw-1.4')
import collections
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer

from extract_ms import MicroStatements


def extract_nouns_adj_cd(statement):
	""" 
	extracts all nouns from each microstatement 'statement'
	Noun PoS tags:
	NN    noun, singular ‘table’
	NNS   noun plural ‘undergraduates’
	NNP   proper noun, singular ‘Rohan'
	NNPS  proper noun, plural ‘Indians’

	JJ    adjective ‘cheap’
	JJR   adjective, comparative ‘cheaper’
	JJS   adjective, superlative ‘cheapest’
	"""
	# tokenize words
	words = nltk.word_tokenize(statement)
	
	# remove all stopwords
	stopwords_set = set(stopwords.words('english'))
	words = [word for word in words if word not in stopwords_set]

	# POS tag all of the words
	tagged_words = nltk.pos_tag(words)

	# get all the nouns (NP, NNP, etc)
	noun = []
	adj = []
	cardinal = []
	infl = inflect.engine()
	lemmatizer = WordNetLemmatizer()

	# print("\nSTATEMENT", statement)
	# print(tagged_words)

	for (word, tag) in tagged_words:
		# singular noun
		if tag == 'NNP' or tag == 'NN':
			# append plural
			pl_word = infl.plural_noun(word)
			noun.append(word)
		# plural noun
		elif tag == 'NNS' or tag == 'NNPS':
			# pl_word = infl.singular_noun(word)
			noun.append(word)
		# adjective
		# don't consider the adj 'many' cus it appears in 'how many''
		elif ((tag == 'JJ' or tag == 'JJR' or tag == 'JJS') and word != 'many'):
			# lemmatize word and add it
			lem_adj = lemmatizer.lemmatize(word)
			adj.append(word)
		elif tag == 'CD':
			cardinal.append(int(word))

	# print("\nNOUN+ADJ ", noun+adj, '\nCD ', cardinal)

	return noun + adj, cardinal

def build_KB(microstatements):
	"""
	input MS, output -> {list of nouns} per microstatement ; {list of quantities in order of microstatements}
	*(see- sourav mandala) //could potentially do by - identify nouns, proper nouns in microstatements

	"""
	# WILL CALL extract_nouns for each statement and build list of tuple of quantities for each ms
	kb = dict()
	quant_kb = dict()

	# build a dict, with each key (ms number): {set of entities & adj}
	# eg 2: {'dan', 'violet', 'marbles'}
	# typically every ms has only one quantity

	for i, ms in enumerate(microstatements):
		#print(ms)
		kb[i+1], cd = extract_nouns_adj_cd(ms)
		# quant_kb[i+1] = []
		for ele in cd:
			# quant_kb[i+1].append(int(ele))
			quant_kb[i+1] = ele
		kb[i+1] = set(kb[i+1])
	
	#print(kb, quant_kb)

	return kb, quant_kb

def IIRU(microstatements, operation):
	"""
	@input: operator, mstmts
	@output: operators that are relevant to the question
	"""
	# DIVISION MULTIPLICAIOTN PROBLEMATIC

	quesornot = quesid.identify_question(microstatements)
	#print(quesornot)

	# print('\n', quesornot)

	# KB for the question
	qKB_temp = build_KB(quesornot['question'])
	qKB = qKB_temp[0]
	qcardinals = qKB_temp[1]

	# world KB for the world statements, cardinals for the numerical quantities
	#for i in quesornot['statements']:
	wKB_temp = build_KB(quesornot['statements'])
	#print(wKB_temp)
	wKB = wKB_temp[0]
	#cardinalsKB = wKB_temp[1]
	cardinalsKB= {}
	if qcardinals != {}:
		cardinalsKB = {0: qcardinals[1]}
	for i in wKB_temp[1]:
		cardinalsKB[i] = wKB_temp[1][i]

	#print(len(cardinalsKB))
	#wKB, cardinalsKB = build_KB(quesornot['statements'])
	#print(cardinalsKB)
	# print("\nKnowledge Base for QUESTION:")
	# print(qKB)

	# print("\nKnowledge Base for WORLD:")
	# for key, val in wKB.items():
	# 	wKB[key] = set(val)
	# 	print(key, wKB[key])
	# print(cardinalsKB)

	# the idea: for each N microstatement in the wKB:
	# IF RELEVANT-> muQ - muN = null set
	# IRRELEVANT-> muQ - muN = not null set
	# return all the ms which gave null set

	muQ = set(qKB[1])
	
	print("\nMuQ >> ", muQ)

	# set of adjectives and words to ignore
	# ignoreset = {'many'} 
	# lambda set
	L = dict() # dict of all the cue differences
	
	if operation in ['addition', 'subtraction', 'division','multiplication']:
		for N, muN in wKB.items():
			# print(N, muN) 
			intersec = muN.intersection(muQ)
			diff = muQ.difference(intersec)

			print('muQ intersec muN ', intersec)
			print('muQ - intersec ', diff, '\n')
			# if diff and diff != {'many'}:
			if diff:
				L[N] = diff
			else:
				L[N] = 'nullset'
	else:
		# handle division and multiplication
		pass

	# print(L)

	irrelevant = {}
	#temp_KB = wKB
	temp_cardinals = {}
	temp_w = {}
	for i in wKB:
		temp_w[i] = wKB[i]
	for i in cardinalsKB:
		temp_cardinals[i] = cardinalsKB[i]
	print("Temp",temp_cardinals)
	'''for n, val in L.items():
		# remove all the nullset ms from the wKB
		if val != 'nullset':
			try:
				irrelevant[n] = wKB.pop(n)
				print('hi im WB! ', wKB)
				# remove all irrelevant quantities
				cardinalsKB.pop(n)
			except Exception as e:
				print(e)'''
	
	print("Temp after",temp_cardinals)
	if len(cardinalsKB) <2:
		cardinalsKB = temp_cardinals
		wKB = temp_w

	print(cardinalsKB)
	print("\nIRRELEVANT INFO extracted:")
	for key, val in irrelevant.items():
		print(key, irrelevant[key])

	print("\nRELEVANT KB:")
	for key, val in wKB.items():
		print(key, wKB[key])
	print(cardinalsKB)
	print(cardinalsKB)
	return wKB, cardinalsKB

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
        relevantKB, cardinalsKB = IIRU(self.microstatements, self.operation)
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

#test_mwp = AMWPS('there are 9 boxes and 8 crates. there are 2 chocolates in each box. how many chocolates are there altogether?')
#test_mwp.solve()
#print(test_mwp.explanation)

ops = ['add', 'div', 'mul', 'sub']
f = open('bypass_iiru_singleop_operatorwise_accuracy.txt', 'w')

for op in ops:
    df = pd.read_json(f'../data/SingleOP_clean/singleop{op}.json')
    questions = df['sQuestion'].tolist()
    answers = df['lSolutions'].tolist()
    skipped_questions = []
    correct_pred = 0
    times = []
    for i, q in enumerate(questions):
        try:
            solver = AMWPS(q)
            solver.solve()
            ans = solver.solution
            if int(ans) == int(answers[i][0]):
                correct_pred += 1
        except:
            skipped_questions.append(q)
    
        print(f'------------------- {i}/{len(questions)} questions done --------------------------')

    accuracy = (correct_pred / len(questions)) * 100
    accuracy_higher = (correct_pred * 100)/(len(questions) - len(skipped_questions))

    f.write(f'Accuracy for {op} (including skipped questions):\t{accuracy}%\n')
    f.write(f'Accuracy for {op} (not including skipped questions:\t{accuracy_higher}%\n')
    f.write(f'Number of questions:\t{len(questions)}\n')
    f.write(f'Number of skipped questions:\t{len(skipped_questions)}\n')
    f.write(f'Skipped Questions: {skipped_questions}\n\n')
    #print(data)
f.close()

ops = ['add', 'div', 'mul', 'sub']
f = open('bypass_iiru_svamp_operatorwise_accuracy.txt', 'w')

for op in ops:
    df = pd.read_json(f'../data/SVAMP_Cleaned/{op}.json')
    questions = df['full_question'].tolist()
    answers = df['Answer'].tolist()
    
    correct_pred = 0
    skipped_questions = []

    for i, q in enumerate(questions):
        try:
            solver = AMWPS(q)
            solver.solve()
            if int(solver.solution) == int(answers[i]):
                correct_pred += 1
        except:
            skipped_questions.append(q)

        print(f'------------------- {i}/{len(questions)} questions done --------------------------')

    accuracy = (correct_pred * 100) / len(questions)
    accuracy_higher = (correct_pred * 100) / (len(questions) - len(skipped_questions))

    f.write(f'Accuracy for {op} (including skipped questions):\t{accuracy}%\n')
    f.write(f'Accuracy for {op} (not including skipped questions:\t{accuracy_higher}%\n')
    f.write(f'Number of questions:\t{len(questions)}\n')
    f.write(f'Number of skipped questions:\t{len(skipped_questions)}\n')
    f.write(f'Skipped Questions: {skipped_questions}\n\n')
        
f.close()