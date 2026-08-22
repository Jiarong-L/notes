import numpy as np
import networkx as nx


G = nx.DiGraph()


G.add_nodes_from(['A','B','C','D'])
G.add_edges_from([('A','B'),('A','C'),('A','D'),
                  ('B','A'),('B','D'),
                  ('C','A'),
                  ('D','B'),('D','C')])



adj_mtx = nx.adjacency_matrix(G).todense().T
transition_matrix = adj_mtx / adj_mtx.sum(axis=0)
init_weight = np.array([1/4 for i in range(4)])
# damping_factor_mtx = np.ones_like(transition_matrix) *0.85
n = 4


######################### Opt1- no damping_factor
w = init_weight
for i in range(100):
    w = transition_matrix @ w

# >>> w
# array([0.33333333, 0.22222222, 0.22222222, 0.22222222])


######################### Opt2- no damping_factor
R = transition_matrix
for i in range(100):
    R = transition_matrix  @ R

# >>> R
# array([[0.33333333, 0.33333333, 0.33333333, 0.33333333],
#        [0.22222222, 0.22222222, 0.22222222, 0.22222222],
#        [0.22222222, 0.22222222, 0.22222222, 0.22222222],
#        [0.22222222, 0.22222222, 0.22222222, 0.22222222]])



######################### Opt3- with damping_factor=0.85
R = transition_matrix
for i in range(100):
    R = (transition_matrix * 0.85 + (1-0.85)/n) @ R

# >>> R
# array([[0.3245614, 0.3245614, 0.3245614, 0.3245614],
#        [0.2251462, 0.2251462, 0.2251462, 0.2251462],
#        [0.2251462, 0.2251462, 0.2251462, 0.2251462],
#        [0.2251462, 0.2251462, 0.2251462, 0.2251462]])




######################### networkx  damping_factor=0.85
# >>> nx.pagerank(G)
# {'A': 0.3245609358176832, 'B': 0.2251463547274389, 'C': 0.2251463547274389, 'D': 0.2251463547274389}





