import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

import pandas as pd

import spacy
import benepar
import neuralcoref

from nltk.tokenize import sent_tokenize

class MicroStatments:
  """
  return microstatemnts from input mwp
  coref resolved and conjunction resolved.
  """
  
  def __init__(self):
    """
    initialising the neuralcoref pipeline
    """
    self.nlp_pronoun = spacy.load('en')
    neuralcoref.add_to_pipe(self.nlp_pronoun, greedyness=0.52)
    benepar.download('benepar_en3')
    self.nlp = spacy.load('en_core_web_sm')
    if spacy.__version__.startswith('2'):
        self.nlp.add_pipe(benepar.BeneparComponent("benepar_en3"))
    else:
        self.nlp.add_pipe("benepar", config={"model": "benepar_en3"})

  def replace(self, sentence):
    """ 
    Neural coref resolution function
    @input : sentence without coref resolution
    @output : coref resolved sentence 
    """
    doc = self.nlp_pronoun(sentence)
    return doc._.coref_resolved

  def __extract_sub_verb_object(self, sentence):
    """
    @input : sentence with coref resolution
    @output : {sub: subject of sentence, 
                verb: verb of sentence, 
                object : object of sentence}
    
    Performed using Parsing a dependency tree generated by benepar (berkeley neural parser)
    """

    # initialise empty strings for S, V and O
    subject = ""
    verb_phrase = ""
    preposition_phrase = ""
    #dependency_tree = sent1._.parse_string
    doc = self.nlp(sentence)
    sent = list(doc.sents)[0]
    dependency_tree = sent._.parse_string

    # 3 flags to keep track of which part of sentence we're in
    # assume we always start with subject -> sb = 1
    sb = 1
    vb = 0
    pb = 0

    for i in range(len(dependency_tree)):
      ch = dependency_tree[i]

      if sb == 1: # sub part
        if (ch.islower()==True or ch.isdigit()==True or ch==" " or ch=="," ):
          if( (subject[:-1]!=" " and ch==" ") or ch!=" "):
              subject = subject+ch

        elif ch=="V": # verb part, set vb = 1
          sb = 0
          vb = 1
          continue

      if vb == 1:
        if (ch.islower()==True or ch.isdigit()==True or ch==" " or ch==","):
          if( (verb_phrase[:-1]!=" " and ch==" ") or ch!=" "):
            verb_phrase = verb_phrase+ch
          
        elif ch=="N" and dependency_tree[i+1] == "P": # obj part, set pb = 1
          vb = 0
          pb = 1
          continue

      if pb == 1:
          if (ch.islower()==True or ch.isdigit()==True or ch==" " or ch==","):
            if( (preposition_phrase[:-1]!=" " and ch==" ") or ch!=" "):
              preposition_phrase = preposition_phrase+ch
      
    return {"subject":subject.strip(), "verb":verb_phrase.strip(), "object":preposition_phrase.strip()}


  def __split_conj(self, sent_list):
    """
    split conjunctions at "and"

    """
    sub = ""
    l = list()

    for i in sent_list:
      if i!="and":
          sub = sub+" "+i
      else:
        if sub!="":
          l.append(sub)
          sub = ""

    l.append(sub)
    return l
  
  def __handle_conjunction(self, sentence):
    d = self.__extract_sub_verb_object(sentence)

    subject = d["subject"].replace(",","and")
    verb = d["verb"].replace(",","and")
    obj = d["object"].replace(",","and")
    subject_tokens = [i for i in subject.split(' ') if i != ' ']
    verb_tokens = [i for i in verb.split(' ') if i!= ' ']
    obj_tokens = [i for i in obj.split(' ') if i!=''] 
    sentences = list()
    if "and" in subject_tokens:
      split_subject = self.__split_conj(subject_tokens)
      
      for i in split_subject:
        sentences.append(i+" "+verb+" "+obj)
      return sentences
    if "and" in obj_tokens:
      
      split_obj = self.__split_conj(obj_tokens)
    
      
      for i in split_obj:
        sentences.append(subject+" " + verb+" "+ i)
        
      return sentences
    else:
      sentences.append(subject+" "+verb+" "+obj)
      return sentences
    
  def mwp_split(self, mwp):
    mwp_split_temp = sent_tokenize(mwp)
    mwp_split = list()
    res = []
    
    for i in mwp_split_temp:
      temp = self.__handle_conjunction(i)
      for j in temp:
        mwp_split.append(j.strip())
    
    for i, sent in enumerate(mwp_split):
      if "and" in sent:
        res.extend(self.__handle_conjunction(sent))
        continue
      res.append(sent)
    
    res = self.__keep_relevant(res)
    
    return res

  def __keep_relevant(self, microsents):
    """
    extracts all nouns from question -> store in a set (qnouns)
    compare nouns of question (qnouns) with set of nouns in each microstatement
    keep only those microstatements which have all nouns in qnouns   

    """
    res = []
    is_noun = lambda pos: pos[:2] == 'NN'
    
    question = microsents[-1]
    qtokens = nltk.word_tokenize(question)
    #print(qtokens)
    #print(nltk.pos_tag(qtokens))
    qnouns = {word for (word, pos) in nltk.pos_tag(qtokens) if is_noun(pos)}
    print(qnouns)
    for sent in microsents:
      tokenized = nltk.word_tokenize(sent)
      nouns = {word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)}
      if len(qnouns.difference(nouns)) <= 1:
        res.append(sent)
    return res

if __name__ == "__main__":
  ms = MicroStatments()
