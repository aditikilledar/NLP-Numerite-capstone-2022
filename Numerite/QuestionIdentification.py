from tensorflow import keras
from sklearn.feature_extraction.text import CountVectorizer
import pickle


model_dolph = keras.models.load_model("models/model_wdolph.h5")
vectorizer = pickle.load(open("models/vectorizer.pickle", "rb"))

# 1 for question, 0 for non-question

def isQuestion_DL(sentence):
    input_sentence = vectorizer.transform([sentence])
    return round(model_dolph.predict(input_sentence)[0][0])

def identify_question(mwp):
    for


inputmwp = 'There are 9 boxes. There are 2 pencils in each box. How many pencils are there altogether?'
print(isQuestion_DL('inputmwp'))

# I was expecting the question as output but got a number 0/1 instead
# I also need to know what other pre-processing is needed to send the mwp to model

