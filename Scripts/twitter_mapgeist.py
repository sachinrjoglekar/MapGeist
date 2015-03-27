#Extracts the top tweets given a search phrase,
#and generates a Mind-Map from the data.
#A handy tool to get an overall view of whats being talked about
#a particular topic.

##Requires the 'TwitterSearch' Python library.
##Get it here: https://github.com/ckoepp/TwitterSearch

from TwitterSearch import *
from mapgeist.api import text_mind_map
from mapgeist.visualization import visualize_tree_2D

#Text phrase to be searched on Twitter
search_text = 'artificial intelligence'

#Number of nodes required in MindMap
N = 50

#Filepath (png format) to store the MindMap to
mappath = 'MindMap.png'


try:
    #Create a TwitterSearchOrder object
    tso = TwitterSearchOrder() 
    tso.set_keywords([search_text])
    #Set language here
    tso.set_language('en')


    #You will need to have your own Twitter App tokens
    #More info here:
    ts = TwitterSearch(
        consumer_key = '',
        consumer_secret = '',
        access_token = '',
        access_token_secret = ''
     )

    i = 0
    f = open('tweets.txt', 'w')
    for tweet in ts.search_tweets_iterable(tso):
        line = str(tweet['text'].encode('utf-8'))
        terms = line.split(' ')
        termlist = []
        for x in terms:
            try:
                #Do some rudimentary preprocessing
                if x == 'RT':
                    continue
                elif x[0] == '@':
                    continue
                elif x[0] == '#':
                    termlist.append(x[1:])
                elif '/' in x:
                    continue
                else:
                    if len(x) > 3:
                        termlist.append(x)
            except:
                pass
        line = ' '.join(termlist) + '.'
        if len(line) > 3:
            f.write(line+'\n')
        i += 1
        if i > 1000:
            break
    f.close()

except TwitterSearchException as e:
    print(e)


#Use MapGeist now
mindmap, root = text_mind_map('tweets.txt', N)
visualize_tree_2D(mindmap, root, mappath)
