import re
from pycipher import Affine
from ngram_score import NgramScore
import argparse

fitness = NgramScore('quadgrams.txt')  # load our quadgram statistics
sample_ctext = 'QUVNLAUVILZKVZZZVNHIVQUFSFZHWZQLQHQLJSNLAUVI'

def break_affine(ctext):
    ctext = re.sub('[^A-Z]', '', ctext.upper())
    # try all posiible keys, return the one with the highest fitness
    scores = []
    for i in [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]:
        scores.extend([(fitness.score(Affine(i, j).decipher(ctext)), (i, j)) for j in range(0, 25)])
    max_key = max(scores)
    return max_key[1], Affine(max_key[1][0], max_key[1][1]).decipher(ctext)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ctext', nargs='?', default=sample_ctext, type=str, help='Enciphered text')
    args = parser.parse_args()
    key, text = break_affine(args.ctext)
    print('best candidate with key (a,b) = ' + str(key) + ':' + text)
