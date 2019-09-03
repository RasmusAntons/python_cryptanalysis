from itertools import permutations
import re
from pycipher import Autokey
from ngram_score import NgramScore
from nbest import NBest
import argparse

qgram = NgramScore('quadgrams.txt')
trigram = NgramScore('trigrams.txt')
sample_ctext = 'isjiqymdebvuzrvwhmvysibugzhyinmiyeiklcvioimbninyksmmnjmgalvimlhspjxmgfiraqlhjcpvolqmnyynhpdetoxemgnoxl'


def break_autokey(ctext, N=100):
    ctext = re.sub('[^A-Z]', '', ctext.upper())
    for KLEN in range(3, 20):
        rec = NBest(N)

        for i in permutations('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 3):
            key = ''.join(i) + 'A' * (KLEN - len(i))
            pt = Autokey(key).decipher(ctext)
            score = 0
            for j in range(0, len(ctext), KLEN):
                score += trigram.score(pt[j:j + 3])
            rec.add((score, ''.join(i), pt[:30]))

        next_rec = NBest(N)
        for i in range(0, KLEN - 3):
            for k in range(N):
                for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    key = rec[k][1] + c
                    fullkey = key + 'A' * (KLEN - len(key))
                    pt = Autokey(fullkey).decipher(ctext)
                    score = 0
                    for j in range(0, len(ctext), KLEN):
                        score += qgram.score(pt[j:j + len(key)])
                    next_rec.add((score, key, pt[:30]))
            rec = next_rec
            next_rec = NBest(N)
        bestkey = rec[0][1]
        pt = Autokey(bestkey).decipher(ctext)
        bestscore = qgram.score(pt)
        for i in range(N):
            pt = Autokey(rec[i][1]).decipher(ctext)
            score = qgram.score(pt)
            if score > bestscore:
                bestkey = rec[i][1]
                bestscore = score
        print(bestscore, 'autokey, klen', KLEN, ':"' + bestkey + '",', Autokey(bestkey).decipher(ctext))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ctext', nargs='?', default=sample_ctext, type=str, help='Enciphered text')
    parser.add_argument('-N', type=int, default=100, help='Number of results to keep from each round')
    args = parser.parse_args()
    break_autokey(args.ctext, args.N)
