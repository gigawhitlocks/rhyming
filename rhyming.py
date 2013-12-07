#!/usr/bin/python2


class Phone(object):

    def _enum(*sequential, **named):
        enums = dict(zip(sequential, range(len(sequential))), **named)
        return type('Enum', (), enums)

    Type = _enum('AFFRICATE',
                 'ASPIRATE',
                 'FRICATIVE',
                 'LIQUID',
                 'NASAL',
                 'SEMIVOWEL',
                 'STOP',
                 'VOWEL')

    with open('symbols', 'r') as symbols_file:
        Symbol = _enum(*symbols_file.read().splitlines())

    @classmethod
    def get(cls, symbol):
        return cls.Symbol.__dict__[symbol]

    symbol_table = {}
    with open('phones', 'r') as phones_file:
        for sym in phones_file.read().splitlines():
            s = sym.split()
            symbol_table[s[0]] = s[1]

    def get_type(self, symbol):
        try:
            return Phone.symbol_table[symbol]
        except KeyError:
            return Phone.symbol_table[symbol[:-1]]

    def __init__(self, symbol):
        self.value = symbol
        self.phonetic_type = self.get_type(symbol)

    def __repr__(self):
        return self.value


class Word(object):

    def __init__(self, english, phonetic):
        self.english = english
        self.phonetic = [Phone(x) for x in phonetic]

    def __str__(self):
        return self.english

    def __repr__(self):
        return "{}:\nphonemes: {}\nfrequency: {}\n".format(self.english,
                                                           self.phonetic,
                                                           self.frequency)

"""

Build a data structure.
First group the words into a dict based on the last phoneme:

{
   AA0: tree,
  AA1: tree,
   T: place a tree here which we can traverse to build any word ending with a T sound

}

"""


def get_words():
    with open('words', 'r') as dictionary:
        words = dictionary.read().splitlines()
        for (i,word) in enumerate(words):
            wordarray = word.split()
            words[i] = Word(wordarray[0].lower(), wordarray[1:])


    with open('word-count', 'r') as word_count_dict:
        word_count = word_count_dict.read().splitlines()

    word_count_dict = {}
    for (i, word) in enumerate(word_count):
        wordarray = word.split()
        word_count_dict[wordarray[0]] = int(wordarray[1])

    word_count = word_count_dict

    for word in words:
        try:
            word.frequency = word_count[word.english]
        except KeyError:
            word.frequency = 0

    dictionary = {}
    for word in words:
        dictionary[word.english] = word
    return dictionary

class Node(object):

    def __init__(self, value=None):
        self.children = {}
        self.parent = None
        self.root = None
        self.value = None

    def insert(self, word, node=None):
        if not self.root:
            self.root = Node()
            self.root.value = word
        else:
            if word not in self.children:
                self.children[word] = Node(value=word)
                self.children[word].parent = self
                self.children[word].root = self.root
            else:
                pass


def main():
    words = get_words()
    for word in words:
        print word.__repr__()



if __name__ == "__main__":
    main()
