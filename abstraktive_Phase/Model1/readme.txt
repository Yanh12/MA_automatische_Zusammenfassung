In this folder you find all necessary files for running the first seq2seq model. 
The ipyng-files are the scripts for the model. Although four versions are provided, they are essentially the same -- only the combination of the used text-reference-pairs and some other factors (path, some hyperparameters) based on the combination are different.

You can train the model by yourself with this model using this corpus or other data sets. 

Or you can use the pretrained weights to test the results. The weigts are:
1) for model ngram_with_short_summary: https://drive.google.com/file/d/1D51A1S3IlEo2hTGFCcuEp4vXBDAiDlDQ/view?usp=sharing
2) for model ngram_with_original_summary: https://drive.google.com/file/d/1CdBLigGiNA1d1XwByyonHZ752WvnoR2Z/view?usp=sharing
3) for model textRank_with_short_summary: https://drive.google.com/file/d/1C0t0By1DTfkA6FSX2LQxJ6IY-42JPCDH/view?usp=sharing
4) for model textRank_with_original_summary: https://drive.google.com/file/d/1uzJGvLXV8L68AsHpZ0qnP31R5zOMSwQL/view?usp=sharing

If you want to directly see the predicted summaries from this model, use the link: https://drive.google.com/drive/folders/1-9fhZcgRmge-QgLx6nuI0lDtKf-u7uVd?usp=sharing. There are four folders for every combination of text-reference-pairs. In these folders there are two folders named "ref" and "predicted". "ref" 
means the reference summaries and in "predicted" there are the predicted summaries from the systems.
