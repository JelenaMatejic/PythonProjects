import matplotlib.pyplot as plt
import networkx as nx
import my_networkx as my_nx 

from nerode import NerodovaKonstrukcija

def non_determ(nk):
    edge_list = [] # Čuva čvorove i njihove težine
    for d in nk.d_matrices:
        for i in range(nk.n):
            for j in range(nk.n):
                if d.value[i][j] == 1:
                    start = "a_" + str(i)
                    end = "a_" + str(j)
                    label = d.name[-1]
                    tuple = (start, end, {'w':label})
                    edge_list.append(tuple)
    return edge_list

# crtanje čvorova i labela u njima
def plot_nodes(G, edge_list):
    G.add_edges_from(edge_list)
    pos=nx.spring_layout(G,seed=5) # pozicioniranje čvorova korišćenjem Fruchterman-Reingold force-directed algoritma, seed vodi računa o rasporedu čvorova na slici
    fig, ax = plt.subplots()
    nx.draw_networkx_nodes(G, pos, ax=ax) # crta samo čvorove u grafu
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=8) # dodaje labele u čvorove
    return G, pos, ax

# crtanje grana
def plot_edges(G, pos, ax):
    curved_edges = [edge for edge in G.edges() if reversed(edge) in G.edges()] # odvajamo skup koji ima između dva čvora povratnu granu
    straight_edges = list(set(G.edges()) - set(curved_edges)) # odvajamo skup koji između dva čvora ima samo direktnu granu
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=straight_edges) # ako nema povratne grane između dva čvora, onda crtamo granu na grafu kao pravu strelicu
    arc_rad = 0.2 # stepen zakrivljenja oblih grana
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=curved_edges, connectionstyle=f'arc3, rad = {arc_rad}') # akao ima povratne grane između dva čvora, onda crtamo granu na grafu kao zakrivljenu strelicu
    return G, curved_edges, straight_edges, pos, ax, arc_rad

# crtanje labela na granama
def plot_labels(G, curved_edges, straight_edges, pos, ax, arc_rad):
    edge_weights = nx.get_edge_attributes(G,'w') # uzmemo sve težine na granama
    curved_edge_labels = {edge: edge_weights[edge] for edge in curved_edges} # rasporedimo težine na one grane koje su zakrivljene
    straight_edge_labels = {edge: edge_weights[edge] for edge in straight_edges}  # rasporedimo težine na one grane koje su prave
    my_nx.my_draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=curved_edge_labels,rotate=False,rad = arc_rad) # pozivamo iscrtavanje labela na zakrivljenim granama
    nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=straight_edge_labels, rotate=False) # iscrtavanje labela na pravim granama
    # fig.savefig("3.png", bbox_inches='tight',pad_inches=0) # Čuvanje slike

# def plot_graphs(nk):
#     G = nx.DiGraph()

#     # Crtanje determinističkog automata
#     edge_list = nk.s_determ_connections
#     G, pos, ax = plot_nodes(G, edge_list)
#     G, curved_edges, straight_edges, pos, ax, arc_rad = plot_edges(G, pos, ax)
#     plot_labels(G, curved_edges, straight_edges, pos, ax, arc_rad)

#     # Crtanje nedeterminističkog automata
#     edge_list = non_determ(nk)
#     G, pos, ax = plot_nodes(G, edge_list)
#     G, curved_edges, straight_edges, pos, ax, arc_rad = plot_edges(G, pos, ax)
#     plot_labels(G, curved_edges, straight_edges, pos, ax, arc_rad)

#     # iscrtavanje oba automata 
#     plt.show()

# Crtanje nedeterminističkog automata
def plot_non_determ(nk):
    G = nx.DiGraph()
    edge_list = non_determ(nk)
    G, pos, ax = plot_nodes(G, edge_list)
    G, curved_edges, straight_edges, pos, ax, arc_rad = plot_edges(G, pos, ax)
    plot_labels(G, curved_edges, straight_edges, pos, ax, arc_rad)
    # plt.title("Non deterministic")
    plt.show()
    
# Crtanje determinističkog automata
def plot_determ(nk):
    G = nx.DiGraph()
    edge_list = nk.s_determ_connections
    G, pos, ax = plot_nodes(G, edge_list)
    G, curved_edges, straight_edges, pos, ax, arc_rad = plot_edges(G, pos, ax)
    plot_labels(G, curved_edges, straight_edges, pos, ax, arc_rad)
    # plt.title("Deterministic")
    plt.show()


