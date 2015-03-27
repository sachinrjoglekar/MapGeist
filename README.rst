MapGeist
========

**Exploring Text, Graphically**

As a Python library/Mind-mapping tool, MapGeist aims to exploit concepts from the domains of **Text Mining** and **Graph Theory** to provide a comprehensive means of understanding/exploring text graphically.

[See docs/methodology.pdf for how it works.]

[See Generated_maps to see a few sample Mind-Maps generated using MapGeist.]

[See Scripts for some handy Python-scripts to draw MindMaps using Wikipedia/Twitter.]

Dependencies
------------

NumPy

Gensim

PyGraphViz (for visualization)

NetworkX


Example Usage
-------------

Suppose ur text is in the file 'text.txt'

    #First import

    >>> from mapgeist.api import text_mind_map

    #First get the Mind-Map as a NetworkX Graph instance, and the root,

    #which is the n-gram with the highest weightage, as a String.

    #You specify the file and the number of nodes required in the Map.

    >>> mindmap, root = text_mind_map('text.txt', 100)

    #Visualization

    >>> from mapgeist.visualization import visualize_tree_2D

    >>> visualize_tree_2D(mindmap, root, 'image.png')

    #Saves the mind-map in the filepath specified as the third argument
    


