import sys

def format(word):
    #add spaces between each charachter in the word and ipa spelling

    #print(word_ipa)
    temp_word = '< '

    for i in range(len(word)):
        temp_word += word[i]
        temp_word += ' '
        if((i+1) == len(word)):
            temp_word += '>'
    return temp_word

if __name__ == '__main__':
    word = format(sys.argv[1])
    print(word)
