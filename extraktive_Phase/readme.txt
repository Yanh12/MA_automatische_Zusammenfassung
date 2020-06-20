In this file you find all scripts for the extractive phase.

You can use CL_word2vec.py to train the word embeddings for the corpus, then use textRank_with_w2c.py to get extrative texts
with the TextRank-Algorithm.

lsa_approach.py is used for the lsa-based extractive method.

ngram_method.py is used for the ngram-based method.

The finshing_data.text provides the links for the six versions of the condensed texts, upon which you can easily get access to 
the final data of this phase and use them for further steps. If you get the final data from these links directly, remenber to
get the TextRank-Lang and the Ngram-Kern versions and at best store them in your google drive (because the abstractive phase's programming codes were trained with Google Colab, which provides a simple way to mount at Google Drive, so you can then read data and store weigts in your drive directly), so they can be used directly 
for the absctractive phase.


#################   Evaluation part      #####################
The "Questionnaire group1.pdf" and "questionnaire group2.pdf" were the complete questionnaires used in the thesis for evaluation the 
quality of the six condensed versions of texts. They're very long so they were not added to the appendix completely. 

The "answers group1.pdf" and "answers group2.pdf" were the answers from the participants from the two times of evaluation.
