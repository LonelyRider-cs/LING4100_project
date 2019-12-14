import numpy as np


def distance(str1, str2):
    #Simple Levenshtein implementation for evalOpenNMT.
    m = np.zeros([len(str2)+1, len(str1)+1])
    for x in range(1, len(str2) + 1):
        m[x][0] = m[x-1][0] + 1
    for y in range(1, len(str1) + 1):
        m[0][y] = m[0][y-1] + 1
    for x in range(1, len(str2) + 1):
        for y in range(1, len(str1) + 1):
            if str1[y-1] == str2[x-1]:
                dg = 0
            else:
                dg = 1
            m[x][y] = min(m[x-1][y] + 1, m[x][y-1] + 1, m[x-1][y-1] + dg)
    return int(m[len(str2)][len(str1)])


if __name__ == '__main__':
    #first string is known, second string is predicted
    tgt_list = [line.strip() for line in open('ipa_tgt_test.txt')]
    pred_list = [line.strip() for line in open('model1_step_100000_pred')]
    all_distances = []
    total_distance = 0
    avg_distance = 0.0

    for i in range(len(tgt_list)):
        temp_distance = distance(tgt_list[i], pred_list[i])
        all_distances.append(temp_distance)
        total_distance = total_distance + temp_distance

    avg_distance = total_distance / len(tgt_list)

    print('The average Levenshtein distance for the set of predicted IPA translations is %.3f' % avg_distance)
    print('n=%d' % len(tgt_list))
