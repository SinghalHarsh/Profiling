import networkx as nx
import matplotlib.pyplot as plt

import pandas as pd

from fds_profiling.visualisation.image_encoding import hex_to_rgb, plot_360_n0sc0pe

def networkplot(column_types, associations):
    
    ## preprocessing assns
    assn_df = associations.copy()
    assn_df["assn"] = abs(assn_df["association"])
    ## - filter
    assn_df = assn_df[assn_df["assn"] >= .01]
    
    
    ## creating graph
    G = nx.from_pandas_edgelist(assn_df,
                                source='col_a', target='col_b',
                                edge_attr=["assn", "type_"],
                                create_using=nx.DiGraph())
    
    ## edges
    corr_edges = [(u,v) for (u,v,d) in G.edges(data=True) if d['type_'] == "NUM-NUM"]
    corr_ratio_edges = [(u,v) for (u,v,d) in G.edges(data=True) if d['type_'] in ("NUM-CAT", "CAT-NUM")]
    theil_edges = [(u,v) for (u,v,d) in G.edges(data=True) if d['type_'] in ("CAT-CAT")]
    
    ## size and color attribute of nodeS
    size_df = assn_df.groupby("col_a", as_index=False)["assn"].sum().rename(columns={"assn":"size"})
    ## - normalizing
    max_size = size_df["size"].max()
    size_df["size"] = size_df["size"]/max_size

    for i in list(G.nodes()):
        G.nodes[i]['size'] = size_df[size_df['col_a']==i]['size'].values[0]
    
        if (column_types[i] == "BOOL"):
            G.nodes[i]['color'] = "#c03d3e"
        elif (column_types[i] == "CAT"):
            G.nodes[i]['color'] = "#3a923a"
        elif (column_types[i] == "NUM"):
            G.nodes[i]['color'] = "#337ab7"
        else:
            G.nodes[i]['color'] = "blue"
            
    
    ## drawing
    ## - fixing the size of the figure 
    plt.figure(figsize =(10,4)) 

    ## color, size, width
    node_color = [nx.get_node_attributes(G, 'color')[v] for v in G] 
    node_size = [1000*nx.get_node_attributes(G, 'size')[v] for v in G]  
    edge_width = [20*G[u][v]['assn'] for u, v in G.edges()] 

    ## layout
    pos=nx.spring_layout(G, iterations=50)

    # node labels
    nx.draw_networkx_labels(G, pos,
                            with_labels = True,
                            font_size=15, font_family='sans-serif', font_color="#000000", font_weight="bold")

    ## nodes
    nx.draw_networkx_nodes(G, pos,
                           node_color = node_color, node_size = node_size, node_shape = "o",
                           alpha=0.9, linewidths=10)

    ## edges
#     nx.draw_networkx_edges(G, pos, edgelist=corr_edges,
#                            width=edge_width, alpha=0.2, style='solid', edge_color="grey", arrows=False)
    
#     nx.draw_networkx_edges(G, pos, edgelist=corr_ratio_edges,
#                            width=edge_width, alpha=0.2, style='solid', edge_color="grey", arrows=False)
    
#     nx.draw_networkx_edges(G, pos, edgelist=theil_edges,
#                            width=edge_width, alpha=0.2, style='solid', edge_color="grey", arrows=False)
    nx.draw_networkx_edges(G, pos,
                           width=edge_width, alpha=0.15, style='solid', edge_color="grey", arrows=False)

    ## edge labels
#     edge_labels =dict([((u, v), d['assn']) for u, v, d in G.edges(data=True)])
#     nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.axis('off') 
    plt.tight_layout()
    return plot_360_n0sc0pe(plt)
    
    
    
