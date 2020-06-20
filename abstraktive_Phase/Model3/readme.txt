In this folder you find scirpts needed for training the third model.

Firstly, the Pointer_Generator_data_preprocessing.ipynb should be used on the text-abstract-pairs to transform the data into
the format that the model can process.

Then different combinations should be trained to gain the results. Here the four versions of combinations are all provided,
like in model2, they only differ from each other in path and some hyperparameters. If you want to try this with your own
data, remenber to change these accordingly. 

Again, these ipynb files might too big to have a direct preview here. The links of these colab files will also be provided:
1. Ngram-Kern with the original summary: https://colab.research.google.com/drive/1CqEnVCeorY90wfqQmkHbOmmQP5IwY8hj?usp=sharing
2. Ngram-Kern with the shortended summary: https://colab.research.google.com/drive/1AzE0V69orwl8Udk2IerrCy1IORoXDhka?usp=sharing
3. TextRank-Lang with original summary: https://colab.research.google.com/drive/1aoEQ7fp6SKf0fmCGuji_o_CN7XqZgsjx?usp=sharing
4. TextRank-Lang with shortened summary: https://colab.research.google.com/drive/1cAMKbNsrUDmwuawloKUl853iZ8cwgdHJ?usp=sharing

If you want to have a look at the predicted summaries and/or get the pre-trained weigths, you can following the following links:
1. Ngram-Kern with the original summary: https://drive.google.com/drive/folders/1zzD_6LJ9UXpNNa2vH1WpnVpue5APtNRl?usp=sharing
2. Ngram-Kern with the shortended summary: https://drive.google.com/drive/folders/1jTJlXa3MVa8UgOOj9t42xBllhJVFDXaf?usp=sharing
3. TextRank-Lang with original summary: https://drive.google.com/drive/folders/1eQxerZQ1V8JzPm4qHrDyJNTxXa3ogI80?usp=sharing
4. TextRank-Lang with shortened summary: https://drive.google.com/drive/folders/1zJnO_oolsvv7PMe9-eNk4ajQYPxa_DBt?usp=sharing

In each folder you can find a folder named "tokenized_dir", in which the preprocessed files for each text-abstract-pair were 
stored; and a "finised_files" folder,in which the preprocessed files were divided into train, validation and test sets. There
is another folder called "logs", where the checkpoints and results were stored. In "logs-myexperiment-train" you find the checkpoints; in "log-myexperiment-decode_test_XXXXXXXXXXXX" you find the results.

