#!/usr/bin/env python

import matplotlib.pyplot as plt

import networkx as nx
import matrix_final
import random
G=nx.Graph()

# contains node numbers in level order
names = []
for i in matrix_final.tree:
    for k in i:
        names.append(k)

# trying to calculate node positions
def find_positions(tree):
    global names
    coords = []
    l = float(len(names)/3)
    for level in tree:
        offset = random.uniform(-0.45,0.45)
        y = tree.index(level)
        nodes = len(level)
        delta = l/(float(nodes)+1)
        x = 0.0
        x+=offset
        if nodes>1:
            for node in level:
                x+=delta
                coords.append((x,y))
        else:
            x+=delta
            coords.append((x,y))
    return coords
coords=find_positions(matrix_final.tree)

# setting positions
pos={names[name]:coords[name] for name in names}

# drawing nodes
nx.draw_networkx_nodes(G,pos,
                       node_size=500,
                       nodelist=matrix_final.DICT.keys(),node_color='w',node_shape='o')

# drawing edgesd
nx.draw_networkx_edges(G,pos,
                       edgelist=matrix_final.find_edges(matrix_final.array),
                       width=1,alpha=0.5,edge_color='b')


# applying labels
labels={}
for element in matrix_final.DICT:
    labels[int(element)]=matrix_final.DICT[element]
nx.draw_networkx_labels(G,pos,labels,font_size=9)

plt.axis('off')
plt.show()
