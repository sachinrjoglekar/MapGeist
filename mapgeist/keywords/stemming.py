from gensim.parsing import PorterStemmer
import os

#Initialize raw stemmer
stemmer = PorterStemmer()


class StemmingHelper(object):
    """
    Class to aid the stemming process.
    From word to stemmed and vice versa.
    """

    word_lookup = {}

    @classmethod
    def stem(cls, word):
        """
        Stems a word and stores original word in lookup.
        """

        #If word contains space, return as is
        if ' ' in word:
            cls.word_lookup[word] = word
            return word

        #Stem the word
        stemmed = stemmer.stem(word)

        #If stemmed word exists in lookup,
        #update the corresponding original word only if
        #the new one is smaller in length.
        #If it does not exist, add it.
        if stemmed in cls.word_lookup:
            if len(cls.word_lookup[stemmed]) > len(word):
                cls.word_lookup[stemmed] = word
        else:
            cls.word_lookup[stemmed] = word

        return stemmed

    @classmethod
    def original_form(cls, word):
        """
        Returns original form of a word given the stemmed version,
        as stored in the word lookup.
        """

        if word in cls.word_lookup:
            return cls.word_lookup[word]
        else:
            return word


#Build stopwords list and attach it to StemmingHelper
dirname = os.path.dirname(os.path.realpath(__file__))
f=open(os.path.join(dirname, 'stopwords'), 'r')
stoplist = []
for line in f :
    stoplist.append(line[0:-1])
f.close()
stoplist.extend(['main article', 'include', 'overview',
                 'references', 'conferences', 'publish',
                 'published'])
stoplist = set(stoplist)

StemmingHelper.stoplist = stoplist
