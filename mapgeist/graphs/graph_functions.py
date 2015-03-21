#All of the graphs-related functionality for MapGeist
#Based on NetworkX, the Python library for dealing with
#graphs
from networkx import (Graph, minimum_spanning_tree,)


def generate_complete_graph(nodes, distance_matrix):
    """
    Returns a NetworkX 'Graph' instance given the following-
    1. The list of nodes to include in the graph.
    2. Distance matrix having distances between nodes- as a dict
    of dicts
    The complete map does NOT contain self loops at any node.
    """

    #First generate an empty graph
    graph = Graph()

    #Make a list of edges, with appropriate weights
    graph_edges = []

    for i in range(len(nodes)-1):
        for j in range(i+1, len(nodes)):
            word1 = nodes[i]
            word2 = nodes[j]
            weight = distance_matrix[word1][word2]
            graph_edges.append((word1, word2, weight))

    #Construct the graph from the edge list
    graph.add_weighted_edges_from(graph_edges)

    #return graph
    return graph


def generate_mst(graph):
    """
    Wrapper for minimum spanning tree computation
    """
    return minimum_spanning_tree(graph)
