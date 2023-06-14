
# Graf početnog nedeterminističkog automata
G = nx.DiGraph()
list_of_edges = []
for d in nk.d_matrices:
    for i in range(nk.n):
        for j in range(nk.n):
            if d.value[i][j] == 1:
                start = "a_" + str(i)
                end = "a_" + str(j)
                label = d.name[-1]
                tuple = (start, end, label)
                list_of_edges.append(tuple)

G.add_weighted_edges_from(list_of_edges)
labels = nx.get_edge_attributes(G, 'weight')
print(labels)

pos = nx.planar_layout(G)
nx.draw_networkx_nodes(G, pos, node_size = 500) # crta čvorove
nx.draw_networkx_labels(G, pos) # crta labele u čvorovima
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='black', arrows=True, connectionstyle='arc3, rad = 0.2') # crta grane
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, label_pos=0.8)



plt.show()