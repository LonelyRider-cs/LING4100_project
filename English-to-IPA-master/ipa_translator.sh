#!/usr/bin/env bash

#check if user entered a word to translate to ipa
#if a word was not entered prompt the user to enter a word
#else set the word passed as an argument to the variable current
if [ -z "$1" ]
then
  echo "You did not enter a word for translation, Please enter one now: "
  read current
else
  current=$1
fi

#confirm to user the word they entered
echo "The word you chose for translation: $current"

#format the word into '< w o r d >'
onmt_word=$(python ONMT_DATA_FORMAT.py "$current")
#write over current word in temp_word.txt
echo $onmt_word > temp_word.txt

#translate the word in temp_word.txt using openNMT with the model created from a set of 32k words
results=$(onmt_translate -gpu 0 -model eng_ipa_model1_steps/eng_ipa_model1_step_100000.pt -src temp_word.txt -replace_unk -verbose -output model1_step_10000_temp_pred)
#print only the results we care about, i.e. the translated IPA
echo "The provided IPA translation is:"
echo $results | egrep -o '< .* >'
echo "Please ignore the first and last symbol, these are needed for the translation process."
