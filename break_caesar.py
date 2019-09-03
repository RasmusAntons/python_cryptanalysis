import re
from pycipher import Caesar
from ngram_score import NgramScore
import argparse

fitness = NgramScore('quadgrams.txt')  # load our quadgram statistics
sample_ctext = 'YMJHFJXFWHNUMJWNXTSJTKYMJJFWQNJXYPSTBSFSIXNRUQJXYHNUMJWX'


def break_caesar(ctext):
    ctext = re.sub('[^A-Z]', '', ctext.upper())
    # try all possible keys, return the one with the highest fitness
    scores = []
    for i in range(26):
        scores.append((fitness.score(Caesar(i).decipher(ctext)), i))
    max_key = max(scores)
    return max_key[1], Caesar(max_key[1]).decipher(ctext)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ctext', nargs='?', default=sample_ctext, type=str, help='Enciphered text')
    args = parser.parse_args()
    key, text = break_caesar(args.ctext)
    print('best candidate with key (a,b) = ' + str(key) + ':' + text)
