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

	# print(tagged_words)

	for (word, tag) in tagged_words:
		# singular noun
		if tag == 'NNP' or tag == 'NN':
			# append plural
			# pl_word = infl.plural_noun(word)
			noun.append(word)
		# plural noun
		elif tag == 'NNS' or tag == 'NNPS':
			pl_word = infl.singular_noun(word)
			noun.append(word)
		# adjective
		elif tag == 'JJ' or tag == 'JJR' or tag == 'JJS':
			# lemmatize word and add it
			lem_adj = lemmatizer.lemmatize(word)
			adj.append(word)
		elif tag == 'CD':
			cardinal.append(word)

	return noun + adj, cardinal

def build_KB(microstatements):
	"""
	input MS, output -> {list of nouns} per microstatement ; {list of quantities in order of microstatements}
	*(see- sourav mandala) //could potentially do by - identify nouns, proper nouns in microstatements

	"""
	# WILL CALL extract_nouns for each statement and build list of tuple of quantities for each ms
	kb = dict()
	quant_kb = dict()

	# build a dict, with each key (ms number): val (entities and quantities)
	# eg 2: ['dan', 'violet', 'marbles', 38]
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
	quesornot = quesid.identify_question(microstatements)

	print('\n', quesornot)

	# KB for the question
	qKB, _ = build_KB(quesornot['question'])

	# world KB for the world statements, cardinals for the numerical quantities
	wKB, cardinalsKB = build_KB(quesornot['statements'])
	
	print("\nKnowledge Base for QUESTION:")
	print(qKB)

	print("\nKnowledge Base for WORLD:")
	for key, val in wKB.items():
		wKB[key] = set(val)
		print(key, wKB[key])
	print(cardinalsKB)

	# the idea: for each N microstatement in the wKB:
	# IF RELEVANT-> muQ - muN = null set
	# IRRELEVANT-> muQ - muN = not null set
	# return all the ms which gave null set

	muQ = set(qKB[1])
	print("\nMuQ >> ", muQ)

	K = dict() # dict of all the set differences
	for N, muN in wKB.items():
		print(N, muN)
		diff = muQ.difference(muN)
		if diff and diff != {'many'}: # hack until issue with adjectives is solved
			K[N] = diff
		else:
			K[N] = 'nullset'

	print(K)

	irrelevant = {}

	for n, val in K.items():
		# remove all the nullset ms from the wKB
		if val != 'nullset':
			try:
				irrelevant[n] = wKB.pop(n)
				print('hi!', wKB)
				cardinalsKB.pop(n)
			except Exception as e:
				print(e)

	print("\nIRRELEVANT INFO extracted:")
	for key, val in irrelevant.items():
		print(key, irrelevant[key])
	print(cardinalsKB)

	print("\nRELEVANT KB:")
	for key, val in wKB.items():
		print(key, wKB[key])
	print(cardinalsKB)

	return wKB, cardinalsKB

# test_microstatements = ['ram has 5 pencils', 'rahul has 33 cats', 'how many cats']
# sourav = ['Aditi has 37 blue balloons','Sandy has 28 blue balloons.','Sally has 39 blue balloons.','How many blue balloons do they have in all?']

if __name__ == '__main__':
	mwp_addition = 'Aditi has 37 blue balloons and Sandy has 28 green balloons. Sally has 39 blue balloons. How many blue balloons do they have in all?'

	mwp_subtraction = 'Dan has 32 green and 38 violet marbles. Mike took 23 of Dan’s green marbles. How many green marbles does Dan now have?'

	mwp_division = 'John has 16 eggs and 8 Skittles. If he shares the eggs among 4 friends, how many eggs does each friend get?'
	
	ms = MicroStatements()

	print('----------------------------ADD------------------------------')
	micro = ms.get_microstatements(mwp_addition)
	IIRU(micro, 'addition')

	# # print("\n--------------------SUBTRACT----------------------------")
	# # micro = ms.get_microstatements(mwp_subtraction)
	# # IIRU(micro, 'subtraction')

	# print("\n--------------------DIVISION----------------------------")
	# micro = ms.get_microstatements(mwp_division)
	# IIRU(micro, 'division')

	# kb = build_KB(micro)
	# print("\nKnowledge Base for above MS:")
	# for key, val in kb.items():
	# 	print(key, val)
