In this folder there are scripts for the abstractive phase. Detailed information is provided in each sub-folder.

Firstly, the DT-extrator.py is used to create the shortend version of reference sumamry. This version of summaries only contain the key aspects (focus, topic & tech).

The rouge script is used for implementing the rouge-metric, after the models are trained.


The data sets needed for training: 
Encoder-Inputs:
1.LSA-Lang: https://drive.google.com/file/d/131dLpbDgI4CBKQoj_LJyZ2FBUB6W3Wtl/view?usp=sharing
2. Ngram_Kern: https://drive.google.com/file/d/1x6BZSk2j_BLE_UpGtSvHAVFCPpbg97WW/view?usp=sharing

Decoder-Data:
1. complete reference sumamry: https://drive.google.com/file/d/1bnZ4vC73FBA1prKSE1G7xF9KRhvBwxBn/view?usp=sharing
2. shortend reference summary: https://drive.google.com/file/d/1UpdI8uZtAcZaWD5U8gyQvILvgnA_4b6S/view?usp=sharing

You can download these data to train/retrain the models, please don't forget to change the paths to get the correct data.
