'''
Question or not output:{'question': 'How many pencils are in all the boxes?', 'statements': ['There are 9 boxes', 'There are 2 pencils in each box', 'James had 7 cats']}

KB output:
one tuple for each microstatement
{entity, [actor, list], [numerical value]}

Aditi - 
Knowledge Base - input MS, output -> {list of nouns} per microstatement ; {list of quantities in order of microstatements} 

IIRU - input -> knowledge base, output -> relevant quantites, using set difference between KB of question and statements.

'''
import inflect
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer

from extract_ms import MicroStatements
import QuestionIdentification as quesid

# ‘word_tokenize’ splits up a sentence into its tokens
# ‘sent_tokenize’ splits up a paragraph into its respective sentences

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
		kb[i+1], cd = extract_nouns_adj_cd(ms)
		# quant_kb[i+1] = []
		for ele in cd:
			# quant_kb[i+1].append(int(ele))
			quant_kb[i+1] = ele
		kb[i+1] = set(kb[i+1])

	return kb, quant_kb

def IIRU(microstatements, operation):
	"""
	@input: operator, mstmts
	@output: operators that are relevant to the question
	"""
	# DIVISION MULTIPLICAIOTN PROBLEMATIC

	quesornot = quesid.identify_question(microstatements)

	# print('\n', quesornot)

	# KB for the question
	qKB, _ = build_KB(quesornot['question'])

	# world KB for the world statements, cardinals for the numerical quantities
	wKB, cardinalsKB = build_KB(quesornot['statements'])
	
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
	
	# print("\nMuQ >> ", muQ)

	# set of adjectives and words to ignore
	# ignoreset = {'many'} 
	# lambda set
	L = dict() # dict of all the cue differences
	
	if operation in ['addition', 'subtraction']:
		for N, muN in wKB.items():
			# print(N, muN) 
			intersec = muN.intersection(muQ)
			diff = muQ.difference(intersec)

			# print('muQ intersec muN ', intersec)
			# print('muQ - intersec ', diff, '\n')
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

	for n, val in L.items():
		# remove all the nullset ms from the wKB
		if val != 'nullset':
			try:
				irrelevant[n] = wKB.pop(n)
				# print('hi im WB! ', wKB)
				# remove all irrelevant quantities
				cardinalsKB.pop(n)
			except Exception as e:
				print(e)

	# print("\nIRRELEVANT INFO extracted:")
	# for key, val in irrelevant.items():
	# 	print(key, irrelevant[key])

	# print("\nRELEVANT KB:")
	# for key, val in wKB.items():
	# 	print(key, wKB[key])
	# print(cardinalsKB)

	return wKB, cardinalsKB

# test_microstatements = ['ram has 5 pencils', 'rahul has 33 cats', 'how many cats']
# sourav = ['Aditi has 37 blue balloons','Sandy has 28 blue balloons.','Sally has 39 blue balloons.','How many blue balloons do they have in all?']

if __name__ == '__main__':
	# mwp_addition = 'Aditi has 37 blue balloons and Sandy has 28 green balloons. Sally has 39 blue balloons. How many blue balloons do they have in all?'
	mwp_addition = 'There are 9 cats in a basket. Another box has 3 cats. Another bag has 5 dogs. How many cats in total?'

	mwp_subtraction = "Dan has 32 green and 38 violet marbles. Mike took 23 of Dan's green marbles. How many green marbles does Dan now have?"

	mwp_subtraction_red = "Dan has 32 red and 38 violet marbles. Mike took 23 of Dan's red marbles. How many red marbles does Dan now have?"


	# mwp_multiplication = 'There are 9 boxes. There are 2 pencils in each box. How many pencils are there altogether?'
	mwp_multiplication = 'There are 9 bags. There are 2 pencils in each bag. How many pencils are there in all bags?'

	# mwp_division = 'John has 16 cats and 8 Skittles. If he shares the cats among 4 friends, how many cats does each friend get?'
	mwp_division = 'Rita has 50 apples. Rita divided the apples among 10 people. How many apples did they get?'
	
	print('----------------------------ADD------------------------------')
	ms = MicroStatements(mwp_addition)
	micro = ms.get_microstatements()
	print("MicroStatements: ", micro)
	build_KB(micro)
	IIRU(micro, 'addition')
	print(mwp_addition)

	print("\n--------------------SUBTRACT----------------------------")
	ms = MicroStatements(mwp_subtraction)
	micro = ms.get_microstatements()

	# micro = [' dan has 32 green marbles', 'dan has  38 violet marbles ', ' mike took 23 of dan green marbles ', ' how many green marbles does dan now have ?']

	print("MicroStatements: ", micro)
	IIRU(micro, 'subtraction')
	print(mwp_subtraction)

	print('\n====== RED ======')
	ms = MicroStatements(mwp_subtraction_red)
	micro = ms.get_microstatements()

	# micro = [' dan has 32 green marbles', 'dan has  38 violet marbles ', ' mike took 23 of dan green marbles ', ' how many green marbles does dan now have ?']

	print("MicroStatements: ", micro)
	build_KB(micro)
	IIRU(micro, 'subtraction')
	print(mwp_subtraction_red)

	print("\n--------------------MULTIPLICATION----------------------------")
	ms = MicroStatements(mwp_multiplication)
	micro = ms.get_microstatements()
	print("MicroStatements: ", micro)
	IIRU(micro, 'multiplication')
	print(mwp_multiplication)

	print("\n--------------------DIVISION----------------------------")
	ms = MicroStatements(mwp_division)
	micro = ms.get_microstatements()
	print("MicroStatements: ", micro)
	IIRU(micro, 'division')
	print(mwp_division)

	# kb = build_KB(micro)
	# print("\nKnowledge Base for above MS:")
	# for key, val in kb.items():
	# 	print(key, val)
