# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 09:46:17 2021

@author: david
"""

from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

import networkx as nx
import matplotlib.pyplot as plt

import random


model = ConcreteModel()

# SETS & PARAMETERS********************************************************************
numNodes=9
enegy=20
polen=10

N=RangeSet(0, numNodes)

cost={}
for i in N:
    for j in N:
        cost[i,j]=999

cost[0,1]=5
cost[0,2]=1
cost[0,3]=2
cost[0,4]=2

cost[1,2]=3

cost[2,7]=7

cost[3,4]=3
cost[3,5]=6

cost[4,5]=5
cost[4,6]=6
cost[4,8]=4

cost[6,7]=4
cost[6,8]=2
cost[6,9]=1


weight={}
for i in N:
    weight[i]=0

weight[1]=3
weight[2]=7
weight[3]=8
weight[4]=2
weight[5]=6
weight[6]=4
weight[7]=1
weight[8]=3
weight[9]=5
    
# VARIABLES****************************************************************************
model.x1 = Var(N,N, domain=Binary)
model.x2 = Var(N,N, domain=Binary)

# OBJECTIVE FUNCTION*******************************************************************
model.objF1 = Objective(expr = sum(model.x1[i,j]*cost[i,j] for i in N for j in N), sense=minimize)
model.objF2 = Objective(expr = sum(model.x2[i,j]*weight[i] for i in N for j in N), sense=maximize)

# CONSTRAINTS**************************************************************************
def source_rule(model,i):
    if i==1:
        return sum(model.x1[i,j] for j in N)==1
    else:
        return Constraint.Skip

model.source=Constraint(N, rule=source_rule)

def destination_rule(model,j):
    if j==4:
        return sum(model.x1[i,j] for i in N)==1
    else:
        return Constraint.Skip

model.destination=Constraint(N, rule=destination_rule)

def intermediate_rule(model,i):
    if i!=1 and i!=5:
        return sum(model.x1[i,j] for j in N) - sum(model.x1[j,i] for j in N)==0
    else:
        return Constraint.Skip

model.intermediate=Constraint(N, rule=intermediate_rule)



# APPLYING THE SOLVER******************************************************************

opt = SolverFactory('ipopt')
model.objF1.deactivate()
model.objF2.activate()
results = opt.solve(model) # solves and updates instance
print('objF1 = ',round(value(model.objF1),2))
print('objF2 = ',round(value(model.objF2),2))
maxOF1=value(model.objF1)
minOF2=value(model.objF2)


"""
# PLOT GRAPH***************************************************************************
G = nx.Graph()

G.add_edge(1, 2, weight=cost.get((1,2)))
G.add_edge(1, 3, weight=2)
G.add_edge(2, 5, weight=8)
G.add_edge(3, 4, weight=3)
G.add_edge(4, 5, weight=2)

red_edges = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 5]
black_edges = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 5]

pos = nx.spring_layout(G, seed=10)  # positions for all nodes - seed for reproducibility

# nodes
nx.draw_networkx_nodes(G, pos, node_size=700)

# edges
nx.draw_networkx_edges(G, pos, edgelist=red_edges, width=6)
nx.draw_networkx_edges(
    G, pos, edgelist=black_edges, width=6, alpha=0.5, edge_color="b", style="dashed"
)

# labels
nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")

ax = plt.gca()
ax.margins(0.08)
plt.axis("on")
plt.tight_layout()
plt.show()    
"""