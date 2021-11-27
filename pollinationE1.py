import numpy as np
from scipy.stats import levy
import matplotlib.pyplot as plt
from matplotlib import animation

# Add a vertex to the dictionary


def add_vertex(v):
    global graph
    global vertices_no
    if v in graph:
        print("Vertex ", v, " already exists.")
    else:
        vertices_no = vertices_no + 1
        graph[v] = []

# Add an edge between vertex v1 and v2 with edge weight e


def add_edge(v1, v2, e):
    global graph
    # Check if vertex v1 is a valid vertex
    if v1 not in graph:
        print("Vertex ", v1, " does not exist.")
    # Check if vertex v2 is a valid vertex
    elif v2 not in graph:
        print("Vertex ", v2, " does not exist.")
    elif v1 == v2:
        temp = [v2, e]
        graph[v1].append(temp)
    else:
        # Since this code is not restricted to a directed or
        # an undirected graph, an edge between v1 v2 does not
        # imply that an edge exists between v2 and v1
        temp = [v2, e]
        graph[v1].append(temp)
        # Creation of second edge to create bidirectionality
        temp = [v1, e]
        graph[v2].append(temp)

# Print the graph


def print_graph():
    global graph
    for vertex in graph:
        for edges in graph[vertex]:
            print(vertex, " -> ", edges[0], " edge weight: ", edges[1])


# driver code
graph = {}
# stores the number of vertices in the graph
vertices_no = 0
add_vertex(1)
add_vertex(2)
add_vertex(3)
add_vertex(4)
add_vertex(5)
add_vertex(6)
add_vertex(7)
# Add the edges between the vertices by specifying
# the from and to vertex along with the edge weights.
add_edge(1, 2, 1)
add_edge(1, 3, 1)
add_edge(1, 4, 2)
add_edge(1, 5, 3)
add_edge(1, 6, 1)
add_edge(1, 7, 2)
add_edge(2, 3, 3)
add_edge(2, 4, 5)
add_edge(2, 5, 2)
add_edge(2, 6, 2)
add_edge(2, 7, 3)
add_edge(3, 4, 4)
add_edge(3, 5, 2)
add_edge(3, 6, 1)
add_edge(3, 7, 2)
add_edge(4, 5, 2)
add_edge(4, 6, 1)
add_edge(4, 7, 5)
add_edge(5, 6, 3)
add_edge(5, 7, 1)
add_edge(6, 7, 2)

# In order for there to be a weight in the nodes, we decided to implement the add edge method but having the start node and the end node being the same to denote the weight of that node.

add_edge(1, 1, 50)
add_edge(2, 2, 60)
add_edge(3, 3, 40)
add_edge(4, 4, 20)
add_edge(5, 5, 10)
add_edge(6, 6, 80)
add_edge(7, 7, 30)


print_graph()
# Reminder: the second element of each list inside the dictionary
# denotes the edge weight.
print("Internal representation: ", graph)


def findPath():
    global graph
    nNodes = 0
    energy = 10
    nNodesOpti = 0
    for vertex in graph:
        for edges in graph[vertex]:
            

