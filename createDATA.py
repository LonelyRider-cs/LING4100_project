import eng_to_ipa as ipa
import pickle

def get_word_IPA(file):
    f = open("word_ipa_dict.pkl","wb")
    word_list = [line.strip() for line in open(file)]
    #print(word_list)
    WORD_IPA_DICT = dict()
    for word in word_list:
        if(ipa.isin_cmu(word) == True):
            WORD_IPA_DICT[word] = ipa.convert(word)
    pickle.dump(WORD_IPA_DICT,f)
    f.close()

if __name__ == '__main__':
    get_word_IPA('wordList.txt')
