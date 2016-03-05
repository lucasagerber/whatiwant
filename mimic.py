"""
whatiwant.mimic
Lucas A. Gerber
"""


import random #, goslate
from .tools import verbosePrint, numGen


class Mimic(object):
    def __init__(self, filename, verbose=True):
        self.filename = filename
        self.mimic_dict = make_mimic_dict(filename)
        self.text = mimic_lecture(self.get_mimic_dict())
        self.verbose = verbose

    def __str__(self):
        return str(self.get_text())

    def lecture(self, count=1, starting_word=None, limit=10):
        while count >= 1:
            verbosePrint(self.verbose, 'Composing lecture...' + str(count))
            self.new_mimic(method='lecture', starting_word=starting_word, limit=limit)
            verbosePrint(self.verbose, 'Complete.')
            count -= 1
        return self.get_text()

    def poem(self, count=1, starting_word=None, limit=10):
        while count >= 1:
            verbosePrint(self.verbose, 'Composing poem...' + str(count))
            self.new_mimic(method='poem', starting_word=starting_word, limit=limit)
            verbosePrint(self.verbose, 'Complete.')
            count -= 1
        return self.get_text()

    def translate(self, count=1, starting_word=None, limit=10):
        while count >= 1:
            verbosePrint(self.verbose, 'Composing translation...' + str(count))
            self.new_mimic(method='translate', starting_word=starting_word, limit=limit)
            verbosePrint(self.verbose, 'Complete.')
            count -= 1
        return self.get_text()
    
    def new_mimic(self, method='lecture', starting_word=None, limit=100):
        if method == 'lecture':
            self.text = mimic_lecture(self.get_mimic_dict(), starting_word=starting_word, limit=limit)
        elif method == 'poem':
            self.text = mimic_poem(self.get_mimic_dict(), starting_word=starting_word, limit=limit)
        elif method == 'translate':
            self.text = mimic_translate(self.get_mimic_dict(), starting_word=starting_word, limit=limit)

    def get_filename(self):
        return self.filename

    def get_mimic_dict(self):
        return self.mimic_dict

    def get_text(self):
        return self.text



def make_mimic_dict(filename):
    """Makes a mimic dictionary from a text file."""
    with open(filename, 'r') as file:
        text = file.read().lower().replace("'",'').split()
    mimic_dict = {}
    prev = ''
    for word in text:
        if not prev in mimic_dict:
            mimic_dict[prev] = [word]
        else:
            mimic_dict[prev].append(word)
        prev = word
    return mimic_dict


def mimic_lecture(mimic_dict, starting_word=None, limit=10):
    """Makes a mimic lecture from a mimic dictionary.
    Limit default is 10 lines (30 seconds)"""

    if not starting_word:
        word = ''
    else:
        word = starting_word

    line_label = (divmod(x*3, 60) for x in numGen())
    text = word
    text = str(next(line_label)) + word
    line_mark = 0
    line_words = 1
    while line_mark < limit:
        if word not in mimic_dict:
            word = ""
        new_word = random.choice(mimic_dict[word])

        if line_words == 0:
            rand_silence = random.randint(1,10)
            if rand_silence <= 2:
                text = text + "\n" + str(next(line_label))
                line_words = 0
                line_mark += 1
                word = new_word
                continue

        text = text + " " + new_word
        rand = random.randint(3,5)
        if line_words >= rand:
            text = text + "\n" + str(next(line_label))
            line_words = 0
            line_mark += 1
        else:
            line_words += 1
        word = new_word
    return text


def mimic_poem(mimic_dict, starting_word=None, limit=10):
    """Makes a mimic poem from a mimic dictionary.
    Limit default is 10 lines"""

    if not starting_word:
        word = ''
    else:
        word = starting_word

    text = word
    line_mark = 0
    line_words = 1
    while line_mark < limit:
        if word not in mimic_dict:
            word = ""
        new_word = random.choice(mimic_dict[word])

        if line_words == 0:
            rand_silence = random.randint(1,10)
            if rand_silence <= 2:
                text = text + "\n"
                line_words = 0
                line_mark += 1
                word = new_word
                continue

        text = text + " " + new_word
        rand = random.randint(3,12)
        if line_words >= rand:
            text = text + "\n"
            line_words = 0
            line_mark += 1
        else:
            line_words += 1
        word = new_word
    return text


'''
def mimic_translate(mimic_dict, starting_word=None, limit=10):
    """Makes a mimic google translation from a mimic dictionary.
    Limit default is 10 lines"""

    text = mimic_poem(mimic_dict=mimic_dict, starting_word=starting_word, limit=limit)

    gs = goslate.Goslate()
    languages = [ lang for lang in gs.get_languages().keys() ]

    translation_iter = random.randint(3,10)
    for i in range(1, translation_iter):
        language = random.choice(languages)
        text = gs.translate(text, language)

    text = gs.translate(text, 'en')

    return text
'''


def main():
    pass

if __name__ == '__main__':
    main()
