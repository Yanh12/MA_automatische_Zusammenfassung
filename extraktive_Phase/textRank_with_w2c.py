import pickle, spacy
import numpy as np
import networkx as nx
from gensim.models import KeyedVectors
from gensim.test.utils import get_tmpfile
from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity
"""
Model 1: TextRak with customerized word embedding as vector representation
Step: 1. Texts in sentences (original texts)
     2. Preprocessing : remove stop words, non-alphabetic characters
     3. Vector representation for each sentence using word embedding, out-of-vocabulary words using the average score
     to represent
     4. Similarity matrix representation : cosine similarity
     5. Build graph
     6. Pick up the top-n sentences (word_count_limitation)
"""
nlp = spacy.load('en',disable = ['ner'])

def TextRank_with_wordEmbedding (filepath,w2v_path,word_count):
  """

  :type word_count: int
  """
  with open (filepath,'rb') as filehandle:
     texts_sents = pickle.load(filehandle)
     #notes: the structure of the data is a list of lists. each inner list represents a text in sentences.

  #note:if use the model trained with lemmatized non-stop tokens, then preprocessing should be done in the same way.
  word_embeddings = {}
  model = open(w2v_path, encoding='utf-8')

  for line in model:
     value = line.split()
     word = value [0]
     embedding = np.asarray(value[1:], dtype='float32')
     word_embeddings[word] = embedding

  #preprocessing sentences
  texts_sents_no_SW = []
  for t in texts_sents:
      t_no_SW = []
      for s in t:
         s_doc = nlp(s)
         s_no_SW = " ".join ([w.lemma_ for w in s_doc if not w.is_stop and not w.lemma_ == ' ' ])
         t_no_SW.append(s_no_SW)
      texts_sents_no_SW.append(t_no_SW)

  #vector representation of each sentence
  #averaging the word-embedding score of each sentence by calculating the score of each of its words.
  #if the word exits in the embedding model, get its representation; if doesn't, set it 0s.
  texts_sent_vec = []
  sentence_vec = []
  for t in texts_sents_no_SW:
     for s in t:
        if len(s) !=0:
           s_vec = sum([word_embeddings.get(w,np.zeros((200,))) for w in s.split()])/(len(s.split())+0.001)
        else:
           s_vec = np.zeros((200,))
        sentence_vec.append(s_vec)
     texts_sent_vec.append(sentence_vec)

  #build similarity matrix (go back to original sentences)
  texts_sim_mat = []
  for i in range (len(texts_sents)):
     sent_count = len(texts_sents[i])
     similarity_matrix = np.zeros([sent_count,sent_count])
     for j in range(sent_count):
        for k in range(sent_count):
           if j !=k:
              similarity_matrix[j][k] = cosine_similarity(np.array(texts_sent_vec[i][j]).reshape(1,200),
                                                       np.array(texts_sent_vec[i][k]).reshape(1,200))[0,0]
     texts_sim_mat.append(similarity_matrix)

  #PageRank-Algorithm
  #build the graph of each text
  texts_scores = []
  for sim_mat in texts_sim_mat:
     nx_graph = nx.from_numpy_array(sim_mat)
     scores = nx.pagerank(nx_graph)
     texts_scores.append(scores)

  summary_textRank = []
  for i in range(len(texts_sents)):
     summary = []
     ranked_sents = sorted(((texts_scores[i][j],s) for j,s in enumerate(texts_sents[i])), reverse= True)

     words = 0
     sents=0
     length = 0
     for k in range (len(ranked_sents)):
        words += len(ranked_sents[k][1].split())
        print(ranked_sents[k][1])
        if words < word_count:
            continue
        else:
           sents = k
           length = words
           break
     #if the doc is shorter than the required or the first sentence is already exceeding the threhold(for summarizing abs)
     if sents == 0:
         if length < word_count:
             sents = len(texts_sents[i])
         else: #use the highest scored sentence instand
             sents = 1

     for s in range(sents):
        summary.append(ranked_sents[s][1])
        if not summary:
            print(textRank_texts[i])
     summary_textRank.append(summary)

  return summary_textRank

textRank_cores = TextRank_with_wordEmbedding('/Users/yanqinghu/Desktop/Masterarbeit/CL_data/core_sentsV2.p',
                                           '/Users/yanqinghu/Desktop/Masterarbeit/CL_data/w2v_cl_normalized.txt', 300)


textRank_texts = TextRank_with_wordEmbedding('/Users/yanqinghu/Desktop/Masterarbeit/CL_data/texts_sentsV2.p',
                                           '/Users/yanqinghu/Desktop/Masterarbeit/CL_data/w2v_cl_normalized.txt', 500)
textRank_abs = TextRank_with_wordEmbedding('/Users/yanqinghu/Desktop/Masterarbeit/CL_data/abs_sentsV2.p',
                                           '/Users/yanqinghu/Desktop/Masterarbeit/CL_data/w2v_cl_normalized.txt', 25)


#pickel the results

with open ("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/textRank_cores.p",'wb') as filehandle:
    pickle.dump(textRank_cores,filehandle)

with open ("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/textRank_texts.p",'wb') as filehandle:
    pickle.dump(textRank_texts,filehandle)

with open ("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/textRank_abstracts.p",'wb') as filehandle:
    pickle.dump(textRank_abs,filehandle)











