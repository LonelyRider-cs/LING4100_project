import pickle
import random
import re

def importDATA():
    file = open('word_ipa_dict.pkl','rb')
    WORD_IPA_DICT = pickle.load(file)
    WORD_IPA_LIST = [[k, v] for k, v in WORD_IPA_DICT.items()]
    random.seed(23434)
    random.shuffle(WORD_IPA_LIST)
    #first_split_marker marks 80% of words
    first_split_marker = int(len(WORD_IPA_LIST) * 0.8)
    #second_split_marker takes 90% of words
    second_split_marker = int(len(WORD_IPA_LIST) * 0.9)
    #train_WORD_IPA_LIST is 0%-80%
    train_WORD_IPA_LIST = WORD_IPA_LIST[:first_split_marker]
    #val_WORD_IPA_LIST is 80%-90%
    val_WORD_IPA_LIST = WORD_IPA_LIST[first_split_marker:second_split_marker]
    #test_WORD_IPA_LIST is 90%-100%
    test_WORD_IPA_LIST = WORD_IPA_LIST[second_split_marker:]
    return train_WORD_IPA_LIST, val_WORD_IPA_LIST, test_WORD_IPA_LIST

def ONMT_DATA_FORMAT(WORD_IPA_LIST, src, tgt):
    #print(WORD_IPA_LIST[0])
    print(WORD_IPA_LIST[0][0])
    print(WORD_IPA_LIST[0][1])
    ONMT_WORD_LIST = []
    ONMT_IPA_LIST = []

    src_f = open(src, "w")
    tgt_f = open(tgt, "w")

    #add spaces between each charachter in the word and ipa spelling
    for word_ipa in WORD_IPA_LIST:
        #print(word_ipa)
        temp_word = '< '
        temp_ipa = '< '
        #for the word
        for i in range(len(word_ipa[0])):
            temp_word += word_ipa[0][i]
            temp_word += ' '
            if((i+1) == len(word_ipa[0])):
                temp_word += '>'
        ONMT_WORD_LIST.append(temp_word)
        src_f.write(temp_word + '\n')
        #for the ipa
        for i in range(len(word_ipa[1])):
            if(word_ipa[1][i] != 'ˈ' and word_ipa[1][i] != 'ˌ'):
                temp_ipa += word_ipa[1][i]
                temp_ipa += ' '
            if((i+1) == len(word_ipa[1])):
                temp_ipa += '>'
        ONMT_IPA_LIST.append(temp_ipa)
        tgt_f.write(temp_ipa + '\n')

    src_f.close()
    tgt_f.close()
    #print(ONMT_WORD_LIST[0])
    #print(ONMT_IPA_LIST[0])

if __name__ == '__main__':
    train_WORD_IPA_LIST, val_WORD_IPA_LIST, test_WORD_IPA_LIST = importDATA()
    #print(len(train_WORD_IPA_LIST))
    #print(len(test_WORD_IPA_LIST))

    ONMT_DATA_FORMAT(train_WORD_IPA_LIST, "word_src_train.txt", "ipa_tgt_train.txt")
    ONMT_DATA_FORMAT(val_WORD_IPA_LIST, "word_src_val.txt", "ipa_tgt_val.txt")
    ONMT_DATA_FORMAT(test_WORD_IPA_LIST, "word_src_test.txt", "ipa_tgt_test.txt")
