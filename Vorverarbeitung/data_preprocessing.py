import pickle, re, os
import spacy
#read data
with open ("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/texts.p",'rb') as filehandle:
    texts_v1 = pickle.load(filehandle)

#see the length of the pickle data
print(type(texts_v1),len(texts_v1))
print(texts_v1[2000].keys())


#function to extract certain parts from the text
def get_certain_parts (texts):
 #get titles of every text & abstratct
 titles = []
 abstracts = []
 for t in texts:
     titles.append(t['Title'])
     abstracts.append(t['\nAbstract\n'])

 #extracts whole texts
 whole_texts = []
 for t in texts:
     text = ""
     secNames = list(t.keys())
     exception = ['\nAbstract\n','\nAcknowledgements\n','\nAcknowledgement\n','\nReferences\n','\nReference\n']
     for name in secNames:
         if name not in exception:
             text += t[name]
     whole_texts.append(text)
 #extract core parts, i.e. introduction and summary/conclusion of each text
 core_parts = []
 for t in texts:
     core_text = ""
     secNames = list(t.keys())
     core_names = ['Introduction','Introductions','Summary','Summaries','Conclusion','Conclusions']
     for name in secNames:
         for core_name in core_names:
             if core_name in name:
                 core_text += t[name]
     core_parts.append(core_text)
 return titles,abstracts,whole_texts,core_parts

titles_v1,abstracts_v1,whole_texts_v1,core_parts_v1 = get_certain_parts(texts_v1)

texts = []
for i in range(len(texts_v1)):
 if not abstracts_v1[i] or not whole_texts_v1[i] or not core_parts_v1[i] or not titles_v1[i]:
     continue
 else:
     texts.append(texts_v1[i])
print("The number of texts, which contain title, abstracts and core parts, is " + str(len(texts)) + ".")

i = 0
for t in texts:
 if not t:
     i+=1
if i == 0:
 print ("No not-well-formed texts now.")

#if all right, extract certain parts from the new dataset
titles, abstracts, whole_texts, core_parts = get_certain_parts(texts)

#data cleaning
def data_cleaning (texts):
  """
  this cleaning only fix the things that may lead to error and remove some substantial information
  not remove special characters, stop-words or do lemmatization/tokenization
  """
  text_cleaned = []
  for text in texts:
     #remove all line breaks /n (repalce them with a white space, for the purpose of the next step)
     text = text.replace('\n', ' ')
     #handle 2-parts-words like "ver- sion" ("- " due to new line in the original data)
     text = re.sub(r'- +','',text)
     #lowercase all words
     text = text.lower()
     #remove all contents insides [] or (), because they are just additional information
     text = re.sub("(\[|\().*?(\]|\))", " ", text)
     #remove all unnecessary white spaces
     text = re.sub(r" +", " ", text)
     #remove https
     text = re.sub(r'(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$'," ",text)
     #remove quot
     text = re.sub (r'\bquot\b', '', text)
     text_cleaned.append(text)
  return text_cleaned

texts_cleaned = data_cleaning(whole_texts)
core_parts_cleaned = data_cleaning(core_parts)
abstracts_cleaned = data_cleaning(abstracts)
titles_cleaned = data_cleaning(titles)

#to check if after preprocessing there are empty elements
empty_ids = []
for i in range(len(texts_cleaned)):
  if not texts_cleaned[i] or not core_parts_cleaned [i] or not abstracts_cleaned [i] or not titles_cleaned[i]:
      empty_ids.append(i)
#if there are empty elements, delete the text
j = 0
for i in range(len(empty_ids)):
  texts_cleaned.pop(empty_ids[i]-j)
  titles_cleaned.pop(empty_ids[i]-j)
  abstracts_cleaned.pop(empty_ids[i]-j)
  core_parts_cleaned.pop(empty_ids[i]-j)
  j += 1

#check if now there are no empty elements:
empty_ids = []
for i in range(len(texts_cleaned)):
  if not texts_cleaned[i] or not core_parts_cleaned[i] or not abstracts_cleaned[i] or not titles_cleaned[i]:
      empty_ids.append(i)
if len(empty_ids) == 0:
  print("There are now " + str(len(texts_cleaned)) + " texts in the corpus after elementary cleaning.")

"""
Differences in preprocessing version 2:
1. do not remove non-alphabetic characters since they are also part of the vocabulary for nlg
2. do not remove stop words and only to tokenize instead of lemmatization for the same reason
"""
def nlp_preprocessing_v2 (texts):
  nlp = spacy.load('en',disable = ['ner'])
  #split text into sentences using spacy sentence detection
  texts_sents = []
  for t in texts:
      #concatenating words like 'long-term'
      t_doc = nlp(t)
      t_sents =list(t_doc.sents)
      t_sents_modified = []
      #to deal with words like long-term-memory to longterm memory since spacy cannot tokenize them correctly
      for s in t_sents:
          s = "".join(str(s).split('-'))
          t_sents_modified.append(s)
      texts_sents.append(t_sents_modified)

  #sentence-wise tokenize
  texts_sentwise_tokens = []
  for t in texts_sents:
      t_tokens = []
      for s in t:
          s_doc = nlp(s)
          s_tokens = [w.text for w in s_doc]
          # remove extra whitespace
          s_tokens = [token for token in s_tokens if token.strip()]
          t_tokens.append(s_tokens)
      texts_sentwise_tokens.append(t_tokens)

  #texts tokens (list flatten from the previous result)
  #this form is for further training word embedding
  texts_tokens = []
  for t in texts_sentwise_tokens:
      text_tokens = [token for sent in t for token in sent]
      texts_tokens.append(text_tokens)

  #get the string form representation for the text
  #for further using summarization libraries
  texts_str = []
  for t in texts_sents:
      text_str = " ".join(s for s in t)
      texts_str.append(text_str)

  return texts_sents, texts_str, texts_sentwise_tokens, texts_tokens



texts_sentsV2, texts_strV2, texts_sentwise_tokensV2, texts_tokensV2 = nlp_preprocessing_v2(texts_cleaned)
cores_sentsV2, cores_strV2, cores_sentwise_tokensV2, cores_tokensV2 = nlp_preprocessing_v2(core_parts_cleaned)
abs_sentsV2, abs_strV2, abs_sentwise_tokensV2, abs_tokensV2 = nlp_preprocessing_v2(abstracts_cleaned)


#picking the parts for late use
#if os.path.exists("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/texts_cleaned.p"):
  #os.remove("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/texts_cleaned.p")

with open ("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/texts_sentsV2.p",'wb') as filehandle:
  pickle.dump(texts_sentsV2,filehandle)
with open ("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/texts_strV2.p",'wb') as filehandle:
  pickle.dump(texts_strV2,filehandle)
with open ("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/texts_sentswise_tokenV2s.p",'wb') as filehandle:
  pickle.dump(texts_sentwise_tokensV2,filehandle)
with open ("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/texts_tokensV2.p",'wb') as filehandle:
  pickle.dump(texts_tokensV2,filehandle)


with open ("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/core_sentsV2.p",'wb') as filehandle:
  pickle.dump(cores_sentsV2,filehandle)
with open ("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/cores_strV2.p",'wb') as filehandle:
  pickle.dump(cores_strV2,filehandle)
with open ("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/cores_sentswise_tokensV2.p",'wb') as filehandle:
  pickle.dump(cores_sentwise_tokensV2,filehandle)
with open ("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/cores_tokensV2.p",'wb') as filehandle:
  pickle.dump(cores_tokensV2,filehandle)

with open ("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/abs_sentsV2.p",'wb') as filehandle:
  pickle.dump(abs_sentsV2,filehandle)
with open ("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/abs_strV2.p",'wb') as filehandle:
  pickle.dump(abs_strV2,filehandle)
with open ("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/abs_sentswise_tokensV2.p",'wb') as filehandle:
  pickle.dump(abs_sentwise_tokensV2,filehandle)
with open ("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/abs_tokensV2.p",'wb') as filehandle:
  pickle.dump(abs_tokensV2,filehandle)


#store data into .txt form (for clear viewing)
def store_texts(texts,file_name):
  if os.path.exists(file_name):
      os.remove(file_name)
  with open(file_name, 'w') as filehandle:
      for t in texts:
          filehandle.write('%s\n' % t)
  return
store_texts(texts_strV2,'/Users/yanqinghu/Desktop/Masterarbeit/CL_data/textsV2.txt')
store_texts(cores_strV2,'/Users/yanqinghu/Desktop/Masterarbeit/CL_data/coresV2.txt')
store_texts(abs_strV2,'/Users/yanqinghu/Desktop/Masterarbeit/CL_data/abstractsV2.txt')




