#All of visualization code for MapGeist
from time import sleep
import pygraphviz as PG
import os


def _is_tree(G):
    """
    Checks if the NetworkX Graph G is a tree.
    """
    from networkx import (number_of_nodes, number_of_edges,
                          is_connected)
    if number_of_nodes(G) != number_of_edges(G) + 1:
        return False
    return is_connected(G)


def _construct_subtree_2G(G, tree, node, added_nodes):
    """
    Constructs the subtree of 'tree' that begins at
    'node'.
    G is the pygraphwiz AGraph instance.
    Assumes that 'node' is already connected to its parents.
    'added_nodes' is a set of strings specifying nodes already
    added to the visualized tree.
    """

    #Iterating over every neighbour of the root of this subtree
    for neighbour in tree.neighbors(node):
        #Make sure the neighbour is not a parent
        if neighbour not in added_nodes:
            #Make a note of the node being added
            added_nodes.add(neighbour)
            #Add the edge between root and neighbour(child)
            G.add_edge(node, neighbour)
            #Call this function recursively on the child
            _construct_subtree_2G(G, tree, neighbour, added_nodes)
            

def visualize_tree_2D(tree, root, filepath):
    """
    Visualizes a NetworkX tree using PyGraphWiz.
    The graph is rendered as a '.ps' named after the root,
    in the folder specified by 'foldername'.
    'tree' is a NetworkX Graph instance, root is a string
    that appears in 'tree'.

    """

    #Check is the Graph is infact a tree
    if not _is_tree(tree):
        raise ValueError("Given Graph is not a tree!")

    G = PG.AGraph(directed=True, strict=True)
    added_nodes = set([root])

    #Call recursive function to build rest of the tree
    _construct_subtree_2G(G, tree, root, added_nodes)

    #Prepare the file with necessary settings
    G.layout(prog='dot')
    G.draw(filepath, format='png')
