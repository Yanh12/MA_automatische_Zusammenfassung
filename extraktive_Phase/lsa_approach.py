import pickle
from sumy.summarizers.lsa import LsaSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


summarizer = LsaSummarizer(Stemmer('english'))
summarizer.stop_words = get_stop_words('english')

def lsa_summarizer(parser,sent_count):
   lsa_s = summarizer(parser.document, sent_count)
   summary_str = ""
   summary = []
   for sent in lsa_s:
       summary_str += str(sent)
   summary.append(summary_str)
   len_summary = 0
   for sent in summary:
       len_summary += len(sent.split())
   return summary, len_summary

def lsa_summaries (filepath,word_count):
   with open(filepath, 'rb') as filehandle:
       texts_str = pickle.load(filehandle)
   lsa_summary = []
   for t in texts_str:
       parser = PlaintextParser(t, Tokenizer('english'))
       for i in range (len(t.split('.'))):
           summary,len_summary = lsa_summarizer(parser,i)
           if len_summary < word_count:
               continue
           else:
               break
       lsa_summary.append(summary)
   return lsa_summary



#using lsa for whole texts, core parts and abstracts and pickel them for late use
lsa_texts= lsa_summaries('/Users/yanqinghu/Desktop/Masterarbeit/CL_data/texts_strV2.p',500)
with open ("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/texts_lsa.p",'wb') as filehandle:
  pickle.dump(lsa_texts,filehandle)

lsa_cores = lsa_summaries('/Users/yanqinghu/Desktop/Masterarbeit/CL_data/cores_strV2.p',300)
with open ("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/cores_lsa.p",'wb') as filehandle:
  pickle.dump(lsa_cores,filehandle)



