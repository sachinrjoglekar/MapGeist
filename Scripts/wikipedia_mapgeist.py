#Extracts the top Wikipedia article given a search phrase,
#and generates a Mind-Map from it.
##Requires the 'wikipedia' Python library.
##Get it here: https://pypi.python.org/pypi/wikipedia/

from mapgeist.api import text_mind_map
from mapgeist.visualization import visualize_tree_2D
from wikipedia import search, page
import os


#Text phrase to be searched on Wikipedia
search_text = 'artificial intelligence'

#Number of nodes required in MindMap
N = 50

#Filepath (png format) to store the MindMap to
mappath = 'MindMap.png'


#The data fetched from wikipedia will be stored in
#a file named 'temp.txt'
dirname = os.path.dirname(os.path.realpath(__file__))
temp_file_path = os.path.join(dirname, 'temp.txt')
f = open(temp_file_path, 'w')
f.close()


#Just a helper
def _write_to_file(text):
    f = open(temp_file_path, 'w')
    f.write(str(text.encode('utf-8').strip()))
    f.close()


#Do the Wikipedia search, and write the text to a file
titles = search(search_text)
wikipage1 = page(titles[0])
_write_to_file(wikipage1.content)


#Use MapGeist now
mindmap, root = text_mind_map(temp_file_path, N)
visualize_tree_2D(mindmap, root, mappath)
