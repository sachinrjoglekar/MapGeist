#This work is based on the paper-
#"Keyword Extraction from a Single Document
#using Word Co-occurrence Statistical Information"
#by Yutaka Matsuo and Mitsuru Ishizuka
#presented at FLAIRS 2003

from mapgeist.keywords.stemming import StemmingHelper


def get_word_sets_file(filename, stem=True, sentences=True):
    """
    A vocabulary dictionary is a list mapping word/bigram to number
    of occurences.
    Returns two things-
    1. A vocabulary dict wrt the entire text.
    2. A list of vocabulary dicts, one for each sentence.
    If sentences is True, a third thing is also returned-
    3. A list of lists containing non-stemmed terms/phrases appearing in
    every sentence
    """

    #Gather a list of sentences
    f = open(filename, 'r')
    sentences = []
    original_sentences = []
    for line in f.readlines():
        temp = line.strip().lower(
            ).translate(None,
                        '?,:;()[]"`-|><^%"*=&1234567890').split('.')
        temp2 = line.strip().split('.')
        for i, x in enumerate(temp):
            if len(x) > 2:
                sentences.append(unicode(x, 'ascii', 'ignore'))
                original_sentences.append(temp2[i])

    #'vocabulary' maps every word/bigram in the text to the number of
    #its occurences
    vocabulary = {}
    #'sentence_words' contains a list of such vocabulary dictionaries,
    #one for each sentence in the text
    sentence_words = []

    for sentence in sentences:
        #This dictionary will map every bigram/word in the sentence
        #to the number of times its occuring
        sentence_vocab = {}
        #Split sentence into words
        temp = sentence.split()
        #Iterate till second-last word
        #(since we are generating bigrams too)
        for i in range(len(temp)-1):
            #Consider bigram with next word
            if (temp[i] not in StemmingHelper.stoplist and
                temp[i+1] not in StemmingHelper.stoplist):
                bigram = ' '.join([temp[i], temp[i+1]])
                sentence_vocab[bigram] = sentence_vocab.get(bigram, 0) + 1
                vocabulary[bigram] = vocabulary.get(bigram, 0) + 1
            #Unigram
            if (temp[i] not in StemmingHelper.stoplist and
                len(temp[i]) > 2):
                if stem:
                    word = StemmingHelper.stem(temp[i])
                else:
                    word = temp[i]
                sentence_vocab[word] = sentence_vocab.get(word, 0) + 1
                vocabulary[word] = vocabulary.get(word, 0) + 1
        #For the last word
        try:
            if temp[-1] not in StemmingHelper.stoplist and len(temp[-1]) > 2:
                if stem:
                    word = StemmingHelper.stem(temp[-1])
                else:
                    word = temp[-1]
                sentence_vocab[word] = sentence_vocab.get(word, 0) + 1
                vocabulary[word] = vocabulary.get(word, 0) + 1
        except:
            pass
        sentence_words.append(sentence_vocab)

    if sentences:
        return vocabulary, sentence_words, original_sentences
    else:
        return vocabulary, sentence_words


def get_param_matrices(vocabulary, sentence_words, n=None):
    """
    Returns -
    1. Top n most frequent terms
    2. co-occurence matrix wrt top-n terms(dict)
    3. Dict containing Pg of most-frequent n terms(dict)
    4. nw(no of words affected) of each word(dict)
    """

    #Figure out top n terms wrt mere occurences
    if n is None or n > len(vocabulary):
        n = min(300, len(vocabulary))
    topwords = list(vocabulary.keys())
    topwords.sort(key = lambda x: vocabulary[x], reverse = True)
    topwords = topwords[:n]

    #nw maps word to the number of words it 'affects'
    #(sum of number of words in all sentences it
    #appears in)
    nw = {}
    #Co-occurence values are wrt top words only
    co_occur = {}
    #Initially, co-occurence matrix is empty
    for x in vocabulary:
        co_occur[x] = [0 for i in range(len(topwords))]

    #Iterate over list of all sentences' vocabulary dictionaries
    #Build the co-occurence matrix
    for sentence in sentence_words:
        total_words = sum(list(sentence.values()))
        #This list contains the indices of all words from topwords,
        #that are present in this sentence
        top_indices = []
        #Populate top_indices
        for word in sentence:
            if word in topwords:
                top_indices.append(topwords.index(word))
        #Update nw dict, and co-occurence matrix
        for word in sentence:
            nw[word] = nw.get(word, 0) + total_words
            for index in top_indices:
                co_occur[word][index] += sentence[word] * \
                                         sentence[topwords[index]]

    #Pg is just nw[word]/total vocabulary of text
    Pg = {}
    N = sum(list(vocabulary.values()))
    for x in topwords:
        Pg[x] = float(nw[x])/N

    return topwords, co_occur, Pg, nw


def get_weightage_values(vocabulary, topwords, co_occur, Pg, nw):
    """
    Calculates the weightages of keywords in the text.
    """
    result = {}
    N = sum(list(vocabulary.values()))
    #Iterates over all words in vocabulary
    for word in co_occur:
        word = str(word)
        org_term = str(StemmingHelper.original_form(word))
        result[org_term] = 0
        for x in Pg:
            #expected_cooccur is the expected cooccurence of word with this
            #word, based on nw value of this and Pg value of the other
            expected_cooccur = nw[word] * Pg[x]
            #Result measures the difference(in no of words) of expected
            #cooccurence and  actual cooccurence
            result[org_term] += (co_occur[word][topwords.index(x)] - \
                                 expected_cooccur)**2/ float(expected_cooccur)
        if ' ' in word:
            result[org_term] *= 2

    #Returns results
    return result
