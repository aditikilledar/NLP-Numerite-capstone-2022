import stanza

def find_Subject_Object(text):
    # import required packages
    nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse')
    doc = nlp(text)
    clausal_subject = []
    nominal_subject = []
    indirect_object = []
    Object          = []
    for sent in doc.sentences:
        for word in sent.words:
            if word.deprel  == "nsubj":
                nominal_subject.append({word.text:"nominal_subject nsubj"})
            elif word.deprel  == "csubj":
                clausal_subject.append({word.text:"clausal_subject csubj"})
            elif word.deprel  == "iobj":
                indirect_object.append({word.text:"indirect_object iobj"})
            elif word.deprel  == "obj":
                Object.append({word.text:"object obj"})
    return indirect_object, Object, clausal_subject,nominal_subject

text ="""john had 5 apples"""

print(find_Subject_Object(text))