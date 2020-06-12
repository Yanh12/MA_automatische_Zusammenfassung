"""
A 'cheater' method: compare each sentence's n-gram representation with the abstract's ngram representation and select
the most similar ones.
Since we already know the abstracts and the major task of the step one is to select the most representative sentences
of the article, it will be convenient to use this method
"""

#abstracts treat as a whole
#texts in sentence-wise

import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
ngram_vectorizer = CountVectorizer(analyzer='char',ngram_range=(3,3))
with open('/Users/yanqinghu/Desktop/Masterarbeit/CL_data/texts_sentsV2.p', 'rb') as filehandle:
   whole_texts = pickle.load(filehandle)
with open('/Users/yanqinghu/Desktop/Masterarbeit/CL_data/core_sentsV2.p', 'rb') as filehandle:
   core_texts = pickle.load(filehandle)
with open('/Users/yanqinghu/Desktop/Masterarbeit/CL_data/abs_sentsV2.p', 'rb') as filehandle:
   abstracts_text = pickle.load(filehandle)
with open('/Users/yanqinghu/Desktop/Masterarbeit/CL_data/abs_strV2.p', 'rb') as filehandle:
   abstracts = pickle.load(filehandle)

def ngrams_summary (texts, abstracts, word_count):
   #abstracts in string form: treat the whole abstract as an entity, which serves as the base for furthur comparison
   #text in sentence form: each sentence will be compaired with the abstract using cosine distance
   ngram_summary = []
   for i in range(len(texts)):
       text = texts[i]
       abstract = []
       abstract.append(abstracts[i])
       whole_text = abstract + text
       ngram_matrix = ngram_vectorizer.fit_transform(whole_text)
       #ngram_matrix[0:1]= the first row, i.e. the abstract
       #the first score = 1 because it compares to itself
       #this compares every sentence with the abstract and score them
       all_scores = cosine_similarity(ngram_matrix[0:1],ngram_matrix)
       #structure of scores = [[xxx.xxxx.xxx...,xxx]], first get the inner list (the score vector)
       scores = all_scores.tolist().pop(0)
       #then delete the first element (because it is the comparison ti itself and get the score 1 which makes no sense)
       scores.pop(0)
       ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(text)), reverse=True)

       words = 0
       sent_count = 0
       length = 0
       for i in range(len(ranked_sentences)):
           words += len(str(ranked_sentences[i][1]).split(" "))
           if words < word_count:
               continue
           else:
               sent_count = i
               length = words
               break
       #if the text is shorter than required word, get the whole text
       #or the first sentence is out of length (for abstracting out of abstracts)
       if sent_count == 0:
           if length < word_count:
               sent_count = len(ranked_sentences)
           else:
               sent_count = 1 #select the highest scored sentence

       summary = []
       for i in range(sent_count):
           summary.append(ranked_sentences[i][1])

       ngram_summary.append(summary)
       for i in range(len(ngram_summary)):
           if not ngram_summary[i]:
               print(i)

   return ngram_summary


texts_ngram = ngrams_summary(whole_texts,abstracts,500)
with open ("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/texts_ngram.p",'wb') as filehandle:
  pickle.dump(texts_ngram,filehandle)


cores_ngram = ngrams_summary(core_texts,abstracts,300)
with open ("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/cores_ngram.p",'wb') as filehandle:
   pickle.dump(cores_ngram,filehandle)




