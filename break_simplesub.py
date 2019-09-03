import random
import re
from pycipher import SimpleSubstitution as SimpleSub
from ngram_score import NgramScore
import argparse

fitness = NgramScore('quadgrams.txt')  # load our quadgram statistics
sample_ctext = 'pmpafxaikkitprdsikcplifhwceigixkirradfeirdgkipgigudkcekiigpwrpucikceiginasikwduearrxiiqepcceindgmie' \
                 'inpwdfprduppcedoikiqiasafmfddfipfgmdafmfdteiki'


def break_simplesub(ctext):
    ctext = re.sub('[^A-Z]', '', ctext.upper())
    maxkey = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    maxscore = -99e9
    parentscore, parentkey = maxscore, maxkey[:]
    print("Substitution Cipher solver, you may have to wait several iterations")
    print("for the correct result. Press ctrl+c to exit program.")
    # keep going until we are killed by the user
    i = 0
    while 1:
        i = i + 1
        random.shuffle(parentkey)
        deciphered = SimpleSub(parentkey).decipher(ctext)
        parentscore = fitness.score(deciphered)
        count = 0
        while count < 1000:
            a = random.randint(0, 25)
            b = random.randint(0, 25)
            child = parentkey[:]
            # swap two characters in the child
            child[a], child[b] = child[b], child[a]
            deciphered = SimpleSub(child).decipher(ctext)
            score = fitness.score(deciphered)
            # if the child was better, replace the parent with it
            if score > parentscore:
                parentscore = score
                parentkey = child[:]
                count = 0
            count = count + 1
        # keep track of best score seen so far
        if parentscore > maxscore:
            maxscore, maxkey = parentscore, parentkey[:]
            print('\nbest score so far:', maxscore, 'on iteration', i)
            ss = SimpleSub(maxkey)
            print('    best key: ' + ''.join(maxkey))
            print('    plaintext: ' + ss.decipher(ctext))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ctext', nargs='?', default=sample_ctext, type=str, help='Enciphered text')
    args = parser.parse_args()
    break_simplesub(args.ctext)
