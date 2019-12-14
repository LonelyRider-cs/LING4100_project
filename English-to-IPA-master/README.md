# English to IPA Translator for any Word using a neural network

## Overview
The goal was to create an application/script that could take any English word as input and return the IPA spelling of that word. This was done using OpenNMT neural network for language translation.


## Running the Code
###### Fresh Build - All I have is wordList.txt and your code

Run all commands within the *English-to-IPA-master* directory.

The first step is to correctly format our data using python. If you want to shuffle your data differently than mine go into *DATA_FORMAT.py* and change the random seed before running.

1. `python createDATA.py`
2. `python DATA_FORMAT.py`

Now we want to preprocess, train, and translate using OpenNMT.

3. `onmt_preprocess -train_src word_src_train.txt -train_tgt ipa_tgt_train.txt -valid_src word_src_val.txt -valid_tgt ipa_tgt_val.txt -save_data saved_preprocess.low -lower`
4. `onmt_train -data saved_preprocess.low -save_model eng_ipa_model1 -gpu_ranks 0`
5. `onmt_translate -gpu 0 -model eng_ipa_model1_steps/eng_ipa_model1_step_100000.pt -src word_src_test.txt -tgt ipa_tgt_test.txt -replace_unk -verbose -output model1_step_100000_pred`

Evaluating the model.

6. `perl perl_evaluation/multi-bleu.perl ipa_tgt_test.txt < model1_step_100000_pred`
7. `python levenshteinDistance.py`

To generate new IPA spellings of unseen words, run the shell script with the only argument being the word you want translated to IPA.

8. `bash ipa_translator.sh your-word-goes-here`

###### I just want to translate individual words, who cares about the model
Run all commands within the *English-to-IPA-master* directory.

1. First download the *English-to-IPA-master.zip* and extract all the files.

To generate new IPA spellings of unseen words, run the shell script with the only argument being the word you want translated to IPA.

2. `bash ipa_translator.sh your-word-goes-here`


## Report
### Data Extraction

The first step in creating this translator model was acquiring enough data to make a model that could accurately predict IPA spelling for any word. The file *wordList.txt* has about ~50k unique words and contains all the words used in the creation of the model.

Then using the free Carnegie Mellon University(CMU) pronouncing dictionary and a public repository for [English to IPA](https://github.com/mphilli/English-to-IPA/tree/a17c83eadddfd5888a1078b5632860cf474a5c2d) translation that requires the use of the CMU pronouncing dictionary we are able to get the IPA spelling. The issue with this is only words that are found to be in the CMU pronouncing dictionary are able to be translated to the IPA spelling. This leaves us with ~40k words to train and test the model on. Then using the python module Pickle in *createDATA.py* we are able to save a dictionary of *word:ipa* to be used for later in a .pkl file.

The next step that is needed is to correctly format the data so that it will work with OpenNMT; This is done in *DATA_FORMAT.py*. From this six different text files are created that contain either the word or IPA spelling and the name of the file determines what it is used for (i.e. train, validation, or test). The six files are as follow:
1. word_src_train.txt
2. word_src_val.txt
3. word_src_test.txt
4. ipa_tgt_train.txt
5. ipa_tgt_val.txt
6. ipa_tgt_test.txt

### Model Creation

The model was created, trained, and tested using OpenNMT. Normally OpenNMT is used for language translation of entire sentences and not for a single word but we can adapt this premise to translate a single word into IPA. To do this we must think of each word as being a sentence and each letter within the word is thought to be a word in the sentence. For example, the word *hello* is equated to being our sentence and the letters *h, e, l, l, o* are equated to being our words in the sentence.

#### Preprocessing

The command line input for preprocessing the data is `onmt_preprocess -train_src word_src_train.txt -train_tgt ipa_tgt_train.txt -valid_src word_src_val.txt -valid_tgt ipa_tgt_val.txt -save_data saved_preprocess.low -lower`. What this does is set our training source to *word_src_train.txt* file and the training target to *ipa_tgt_train.txt*. The same is done for validation source and validation target with their respective text file names. The preprocessed data is then saved to *saved_preprocess.low* and the argument *-lower* ensures all letters are lowercase in our text files.

 For those that do not know the validation set is the same as a dev set in any other machine learning model.

#### Training

The command line input for training is `onmt_train -data saved_preprocess.low -save_model eng_ipa_model1 -gpu_ranks 0`. What this does is train a model for English to IPA translation using the preprocessed data from the step before. The model is saved to *eng_ipa_model1*. We set the GPU rank to zero to tell the model to train on our first index GPU in your hardware.

Notes: This model was trained on a NVIDIA 1660 TI in approximately an hour and fifteen minutes. By default every 5000 steps a model is saved.

#### Translate

The command line input for translating is `onmt_translate -gpu 0 -model eng_ipa_model1_steps/eng_ipa_model1_step_100000.pt -src word_src_test.txt -tgt ipa_tgt_test.txt -replace_unk -verbose -output model1_step_100000_pred`. First we tell the system we would like to translate using the GPU indexed at zero and to use the model with step 100000. We then set our source and target to there respective testing text files. The argument `-replace_unk` tells the model if an unknown character from our source data was not seen when training to use the character in the predicted output. The argument `-verbose` prints each prediction and score for every translated word. The argument `-output` saves each predicted translation to a new line in *model1_step_100000_pred*.

### Evaluation

##### Bleu Score
The first type of evaluation done provides us with a Bleu score. This is the normal way of evaluating a translation model from OpenNMT. What a Bleu score finds is the amount of similar words from the predicted output compared to the known output but it does not care about what order these words are in. When translating entire sentences from one language to another the order of the words does not matter due to the fact that the languages most likely have different structures. If the predicted is an identical match to the known then you get a Bleu score of 1. If the predicted and the known are not similar in any way then a Bleu score of 0 is achieved.

With this model a Bleu score of 0.9289 was achieved. This is a very high Bleu score meaning their are a lot of similarities between the predicted output and the known output. The issue with this though is that we do care about the order because our model predicts the translation of a word and not actually a sentence. When translating a word from one language to another the spelling of the translated word matters and therefore we do not want to disregard the order when evaluating.


##### Levenshtein Distance
The second type of evaluation done is known as a Levenshtein distance. What this does is measure the distance between two sequences. The distance is found by adding up the number of single-character edits(insertion, deletion, substitution) needed to change one word into another. Since order matters here it will provide us with a more accurate representation of our model.

With this model an average Levenshtein distance of 0.341 was found. This would indicate their are many words that require no manipulation to make the predicted match the known. This also indicates their are very few words who require any sort of manipulation to make the predicted and known match.


## Conclusion
Since we have such a high Bleu score and low Levenshtein distance we can confidently say that our model predicts an accurate translation from English to IPA. Now that we are confident with our model we can create a script to translate any English word into IPA.

## Citations
#### OpenNMT
```
@inproceedings{opennmt,
    author  = {Guillaume Klein and
               Yoon Kim and
               Yuntian Deng and
               Jean Senellart and
               Alexander M. Rush},
  title     = {OpenNMT: Open-Source Toolkit for Neural Machine Translation},
  booktitle = {Proc. ACL},
  year      = {2017},
  url       = {https://doi.org/10.18653/v1/P17-4012},
  doi       = {10.18653/v1/P17-4012}
}
```
The directory *perl_evaluation* contains the perl function to find the Bleu score, this is provided by OpenNMT.

#### English-to-IPA

```
@inproceedings{English-to-IPA,
    author  = {mphilli and
               ValerioNeriGit and
               Tim Van Cann and
               Mitchellpkt},
  title     = {Converts English text to IPA notation},
  year      = {2019},
  url       = {https://github.com/mphilli/English-to-IPA/tree/a17c83eadddfd5888a1078b5632860cf474a5c2d},
}
```
This relates to everything within the *eng_to_ipa* directory.
