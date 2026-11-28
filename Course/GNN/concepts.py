import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def save_plot(G,img_file):
    nx.draw_networkx(G)
    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")
    plt.savefig(img_file)
    plt.close()


G = nx.DiGraph()


G.add_nodes_from(['A','B','C','D'])
G.add_edges_from([('A','B'),('A','C'),('A','D'),
                  ('B','A'),('B','D'),
                  ('C','A'),
                  ('D','B'),('D','C')])

save_plot(G,'1.png')

## 2
nx.diameter(G)

## DiDegreeView({'A': 5, 'B': 4, 'C': 3, 'D': 4})
nx.degree(G)

## Only for non-directed Graph()
nx.connected_components(G)

# array([[0, 1, 1, 1],
#        [1, 0, 0, 1],
#        [1, 0, 0, 0],
#        [0, 1, 1, 0]], dtype=int32)
nx.adjacency_matrix(G).todense()

nx.incidence_matrix(G).todense()

## Only for non-directed Graph()
nx.laplacian_matrix(G).todense()

## {'A': 1.6666666666666665, 'B': 1.3333333333333333, 'C': 1.0, 'D': 1.3333333333333333}
nx.degree_centrality(G)

## {'A': 0.5, 'B': 0.5, 'C': 0.5, 'D': 0.5}
nx.eigenvector_centrality(G)

## {'A': 0.41666666666666663, 'B': 0.08333333333333333, 'C': 0.08333333333333333, 'D': 0.08333333333333333}
nx.betweenness_centrality(G)

## {'A': 0.75, 'B': 0.75, 'C': 0.75, 'D': 0.75}
nx.closeness_centrality(G)

## {'A': 0.3245609358176832, 'B': 0.2251463547274389, 'C': 0.2251463547274389, 'D': 0.2251463547274389}
nx.pagerank(G)

## HUB       ({'A': 0.4534016256620827, 'B': 0.1777078633879224, 'C': 0.04659837433791723, 'D': 0.3222921366120775}, 
## Authority {'A': 0.09319674867583447, 'B': 0.3222921366120778, 'C': 0.3222921366120774, 'D': 0.2622189781000104})
nx.hits(G)






