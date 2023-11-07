import networkx as nx
import matplotlib.pyplot as plt
# =======================================================================

def A():
    """
    xxxxxxxxxxxxxxxxxxxxxxxxxx
    """
    G = nx.Graph()
    G.add_edge('center',1)
    G.add_edge('center',2)
    G.add_edge('center',3)
    G.add_edge('center',4)
    pos = {'center':(0,0), 1:(1,0), 2:(0,1), 3:(-1,0), 4:(0,-1)}
    nx.draw(G, pos=pos, with_labels=True)
    plt.show()

A
