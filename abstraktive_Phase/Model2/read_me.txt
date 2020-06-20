It might be difficult to have the overview of codes directly in GitHub. Therefore, the original links of the google colab for
the codes are also provided.

Basically, although different code file are given for different combination of text-abstracts pairs. However, they differ from 
each other only concerning the input data (path) and some hyperparameters (the longest encoding and decoding steps).

Bilstm-Ngram-original-abstracts: https://colab.research.google.com/drive/1StfaQnv3TK0yw6O9nx9WqyYbLFCguHeI?usp=sharing
Bilstm-Ngram-shortened-abstracts: https://colab.research.google.com/drive/1ZI2pPeFIL8W_wTBhXEDu6Wyy98tKQvKS?usp=sharing
Bilstm-TextRank-original-abstracts: https://colab.research.google.com/drive/1Ppk9urAlKATRGH0tjD1QjD03S458upmi?usp=sharing
Bilstm-TextRank-shortened-abstracts: https://colab.research.google.com/drive/1nLRLHQwv8RZbbvbv1RsSzWv-2_8f59kV?usp=sharing

You can use this scripts to train the model with this corpus or other data. You can also read these scripts to see some results from my trainings.

Besides, you can access to the trained weigts and the results via (also for all different combinations of text-abstract-pairs): 
https://drive.google.com/drive/folders/14FREZAFnVikCFC_l1GMRJkbJSMGwzQcT?usp=sharing

Clicking this link, you will see 4 folders: ngram_short_sum, ngram_ori_sum, tr_short_sum, tr_ori_sum. They stand for the four
combinations of text-abstract-pairs, respectively. In every folder, you will find a sub-folder named "predicted", in which the
predicted summaries from the system were stored and a sub-folder called "ref", in which the reference abstratcs used for testing were stored. You will also find all checkpoints from the training, which you can easily used for testing.
