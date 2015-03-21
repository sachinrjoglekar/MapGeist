#Mind-map generation tools for MapGeist
#Requires the Python wikipedia library
from mapgeist.keywords import *
from mapgeist.graphs import *
from numpy.linalg import norm
from numpy import array, dot
from random import random
from math import log
import os

def _cos(v1, v2):
    dot_product = dot(v1, v2)
    m1 = norm(v1)
    m2 = norm(v2)
    return dot_product/float(m1*m2)


#File handling
dirname = os.path.dirname(os.path.realpath(__file__))
temp_file_path = os.path.join(dirname, 'temp.txt')
f = open(temp_file_path, 'w')
f.close()


def _write_to_file(text):
    f = open(temp_file_path, 'w')
    f.write(str(text.encode('utf-8').strip()))
    f.close()


#Mind mapping code

def text_mind_map(filename, N=50):
    """
    Builds a mind map from a text file.
    """

    #Use the functions in mapgeist.keywords, to understand
    #the weightages of terms present in the text file
    #and to compute the co-occurence matrix
    vocabulary, sentence_words, original_sentences = (
        get_word_sets_file(filename))
    topwords, co_occur, Pg, nw = (get_param_matrices(
        vocabulary, sentence_words))
    weightages = get_weightage_values(vocabulary, topwords, co_occur,
                                      Pg, nw)

    #Figure out the root
    root = max(list(weightages.keys()), key=lambda x: weightages[x])

    #First make a list of all the terms available
    terms = [x for x in list(weightages.keys()) if
             StemmingHelper.stem(x) in topwords]
    for i, x in enumerate(terms):
        terms[i] = x.capitalize()

    #Remove all terms that are a part of another term, and have lesser
    #weightage
    new_terms = []
    for x in terms:
        flag = False
        for y in terms:
            if x in y and x != y:
                if weightages[x.lower()]*0.8 < weightages[y.lower()]:
                    flag = True
                    break
        if not flag:
            new_terms.append(x)
    terms = new_terms

    #Initialize the distance matrix
    distance_matrix = {}
    for term in terms:
        distance_matrix[term] = {}

    for i in range(len(terms)-1):
        for j in range(i+1, len(terms)):
            m = ((co_occur[StemmingHelper.stem(terms[i].lower())][
                topwords.index(StemmingHelper.stem(
                    terms[j].lower()))]) + 0.1)
            distance_matrix[terms[i]][terms[j]] = m
            distance_matrix[terms[j]][terms[i]] = (
                distance_matrix[terms[i]][terms[j]])

    for term in terms:
        distance_matrix[term][term] = 0

    #The distance between two terms is dependent on how much each of them
    #is important to the other
    #Compute the normalized co-occurences
    for term in distance_matrix:
        total = float(sum(list(distance_matrix[term].values())))
        for term2 in distance_matrix[term]:
            distance_matrix[term][term2] = (
                distance_matrix[term][term2]/total)

    new_dist_matrix = {}
    for term1 in distance_matrix.keys():
        new_dist_matrix[term1] = {}
        for term2 in distance_matrix.keys():
            new_dist_matrix[term1][term2] = (
                distance_matrix[term1][term2]*
                distance_matrix[term2][term1])

    distance_matrix = new_dist_matrix
    
    #Prune the list of terms further, based on weightage
    terms.sort(key=lambda x: weightages[x.lower()], reverse=True)
    terms = terms[:N]

    #Build the distance matrix
    #The distance between two terms is a product of their normalized
    #co-occurence, and the cosine of the angle between their vectors
    #denoting co-occurences with other terms
    new_distance_matrix = {}
    for term1 in terms:
        new_distance_matrix[term1] = {}
        for term2 in terms:
            if term1 == term2:
                new_distance_matrix[term1][term2] = 0
                continue
            try:
                new_distance_matrix[term1][term2] = (
                    new_distance_matrix[term2][term1])
                continue
            except:
                pass
            t1 = distance_matrix[term1][term2]
            temp1 = []
            temp2 = []
            tempterms = terms[:]
            tempterms.remove(term1)
            tempterms.remove(term2)
            for term in tempterms:
                temp1.append(distance_matrix[term1][term])
                temp2.append(distance_matrix[term2][term])
            temp1 = array(temp1)
            temp2 = array(temp2)
            t2 = _cos(temp1, temp2)
            new_distance_matrix[term1][term2] = 1.0/(t1*t2+
                                                     0.00000000001)

    distance_matrix = new_distance_matrix

    #Build the complete graph first
    graph = generate_complete_graph(terms, distance_matrix)

    #Return an mst generated from the graph, and the root
    return generate_mst(graph), root.capitalize()

