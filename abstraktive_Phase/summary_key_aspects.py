import pickle

with open('/Users/yanqinghu/Desktop/Masterarbeit/CL_data/abs_sentsV2.p', 'rb') as filehandle:
    abstracts = pickle.load(filehandle)

with open('/Users/yanqinghu/Desktop/Masterarbeit/CL_data/abs_infos.p', 'rb') as filehandle:
    abs_info = pickle.load(filehandle)

"""
Agenda: 1. import cleaned texts, cores, abstracts & titles
        2. visulize the distribution of texts and its parts
"""

import pickle, re, os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


#get the distribution overview of the corpus
def get_histgram (texts,file_path,file_path2, c1, c2, c3, c4, t1, t2):
    """
    With this function the distribution of word counts in the texts and its core parts and the number of sentences
    in them will be calculated and visulized.

    :param :texts: the texts file
            file_path1 & file_path2: where to store the histgrams
            c1-c4: colors in the histgrams
            t1,t2: titles of the 2 histgrams
    """
    #split sentences into tokens
    t_tokens = []
    for t in texts:
        t_tokens.append(t.split())
    # record the length of every selected abstract
    len_tokens = []
    for t in t_tokens:
        len_tokens.append(len(t))

    # histgram to show the length distribution (word count)
    len_tokens_np = np.array(len_tokens)
    len_mean = len_tokens_np.mean()
    len_min = len_tokens_np.min()
    len_max = len_tokens_np.max() - 500
    sns_hist = sns.distplot(len_tokens_np, kde=True, color=c1)
    plt.axvline(len_mean, color=c2, linestyle=":", alpha=2)
    plt.text(len_mean + 30, 0.0002, 'Average word count: %.1f' % (len_mean), color=c2)
    #plt.axvline(len_min, color=c2, linestyle="--", alpha=2)
    #plt.text(len_min + 3, 0.00006, 'Minimal word count: %.1f' % (len_min), color=c2)
    #plt.axvline(len_max, color=c2, linestyle="-.", alpha=2)
    #plt.text(len_max - 1000, 0.00004, 'Maximal word count: %.1f' % (len_max), color=c2)
    plt.title(t1)
    plt.show()
    fig = sns_hist.get_figure()
    fig.savefig(file_path)

    #split texts into sentences
    t_sents = []
    for t in texts:
        t_sents.append(t.split('.'))

    #calculating the average number of sentences in the corpus
    len_t_sent = []
    for t in t_sents:
        len_t_sent.append(len(t))

    len_t_sent_np = np.array(len_t_sent)
    len_t_sent_mean = len_t_sent_np.mean()
    len_t_sent_min = len_t_sent_np.min()
    len_t_sent_max = len_t_sent_np.max() - 500
    sns_hist2 = sns.distplot(len_t_sent_np, kde=True, color = c3)
    plt.axvline(len_t_sent_mean, color=c4, linestyle=":", alpha=2)
    plt.text(len_t_sent_mean + 5, 0.0002, 'Average sentence count: %.1f' % (len_t_sent_mean), color=c4)
    plt.axvline(len_t_sent_min, color=c4, linestyle="--", alpha=2)
    #plt.text(len_t_sent_min + 3, 0.01, 'Minimal sentence count: %.1f' % (len_t_sent_min), color=c4)
    plt.axvline(len_t_sent_max, color=c4, linestyle="-.", alpha=2)
    #plt.text(len_t_sent_max - 50, 0.025, 'Maximal sentence count: %.1f' % (len_t_sent_max), color=c4)
    plt.title(t2)
    plt.show()
    fig2 = sns_hist2.get_figure()
    fig2.savefig(file_path2)

    return t_tokens, t_sents



abs_infos_wor, abs_infos_sent = get_histgram (abs_info, "/Users/yanqinghu/Desktop/Masterarbeit/CL_data/abstract_word_countV2.png",
                                        "/Users/yanqinghu/Desktop/Masterarbeit/CL_data/abstract_sent_countV2.png",'lemonchiffon',
                                        'indianred', 'darkseagreen', 'darkorange', 'Word count of the key-aspects abstracts',
                                        'Sentence count of the key-aspects abstracts')