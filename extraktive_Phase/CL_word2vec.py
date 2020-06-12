import pickle
with open ("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/texts_tokens.p",'rb') as filehandle:
    texts_normalized = pickle.load(filehandle)
with open ("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/texts_tokensV2.p",'rb') as filehandle:
    texts = pickle.load(filehandle)

"""
build model (vocab & tune hyperparameters for training)
1st model: based on normalized texts (remove non-alphabetic chars, lemmatization, remove stop words)
2st model: based on rather "raw" texts, only fixed errors and tokenized
"""
from gensim.models import Word2Vec
def w2v (texts,model_name, dim, *, train = False, save_format):
    """
    :hyperparameters of the model:
    :param size: dimensions of the vectors of each word
    :param window: the window size
    :param min_count: only words appear in the corpus beyond min count will be added into the vocabulary
    :param workers: patrition
    :param sg = 1: skip-gram model (sg = 0:CWOB)
    :param sample : threhold for subsampling a too frequent word (beyond the threhold, probabliy be dropped; under the
    threhold, will definitely not be dropped
    :param negative: for negative sampling, default = 5, to speed up the training process, every time only update 1 positive
    word + 5 negative words' weights (for over case, only 6 * 200 weights)
    :return: the trained model in the binary form
    """
    if train == True:
        model = Word2Vec(texts,size = dim, window = 5, min_count = 5,workers = 5, sg=1, sample=1e-3,negative=5,iter = 10)
        if save_format == 'txt':
            model.wv.save_word2vec_format('/Users/yanqinghu/Desktop/Masterarbeit/CL_data/{}.txt'.format(model_name),binary=False)
        elif save_format == 'bin':
            model.save('/Users/yanqinghu/Desktop/Masterarbeit/CL_data/{}.model'.format(model_name))

    return model

#model_normalized = w2v(texts_normalized,200, "w2v_cl_normalized",train=True,save_format='txt')
#model_raw = w2v(texts,'w2v_cl',300, train=True,save_format='txt')
model_raw_bin = w2v(texts,'w2v_cl',300, train=True,save_format='bin')


