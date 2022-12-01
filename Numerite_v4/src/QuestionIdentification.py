# from tensorflow import keras
# from sklearn.feature_extraction.text import CountVectorizer
# import pickle


# model_dolph = keras.models.load_model("../models/model_wdolph.h5")
# vectorizer = pickle.load(open("../models/vectorizer.pickle", "rb"))

# 1 for question, 0 for non-question

# def isQuestion_DL(sentence):
#     input_sentence = vectorizer.transform([sentence])
#     return round(model_dolph.predict(input_sentence)[0][0])

def identify_question(microstatements):
    statements = []
    question = []
    question_words = ["evaluate", "calculate", "find", "determine","how", "what","identify"]
    for i in microstatements:
        flag_q = False
        for j in question_words:
            if j in i:
                question.append(i)
                flag_q = True
                break
        if flag_q == False:
            statements.append(i)

    if len(question)==0:
        question.append(microstatements[-1])
        statements = statements[:len(statements)-1]
    # question = microstatements[-1]
    # statements = microstatements[:len(microstatements)-1]
    # for i in microstatements:
    #     if isQuestion_DL(i):
    #         question.append(i)
    #     else:
    #         statements.append(i)  
    return {"question":question,"statements":statements}

 
# inputmwp = 'There are 9 boxes. There are 2 pencils in each box. How many pencils are there altogether?'
# print(identify_question(inputmwp))
#returns a dictionary with key "question" for the question microstatements, and "statements" for the non-question microstatements
