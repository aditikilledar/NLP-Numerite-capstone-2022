from tensorflow import keras
from sklearn.feature_extraction.text import CountVectorizer
import pickle


model_dolph = keras.models.load_model("models/model_wdolph.h5")
vectorizer = pickle.load(open("models/vectorizer.pickle", "rb"))

# 1 for question, 0 for non-question

def isQuestion_DL(sentence):
    input_sentence = vectorizer.transform([sentence])
    return round(model_dolph.predict(input_sentence)[0][0])

def identify_question(microstatements):
    # microstatements = mwp.split(".") ##microstatements module fits here, for now i have simply split sentence at full stop
    statements = []
    question = ''
    for i in microstatements:
    	if isQuestion_DL(i):
    		question = i
    	else:
    		statements.append(i)  
    return {"question":question,"statements":statements}


# inputmwp = 'There are 9 boxes. There are 2 pencils in each box. How many pencils are there altogether?'
# print(identify_question(inputmwp))
#returns a dictionary with key "question" for the question microstatements, and "statements" for the non-question microstatements

