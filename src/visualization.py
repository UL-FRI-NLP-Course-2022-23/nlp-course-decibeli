from igraph import *

def read_triplets(path):
    with open(path) as f:
        lines = f.readlines()
        return lines

def get_edge_color(rel_type):
    if rel_type == 'parents':
        return 'blue'
    if rel_type == 'siblings':
        return 'gray'
    if rel_type == 'children':
        return 'green3'
    if rel_type == 'spouse':
        return 'magenta'
    else: 
        print(rel_type)
        return 'cyan'
    
def get_color_dict():
    colors = ['blue', 'green3', 'gray', 'magenta', 'cyan']
    labels = ["parents", 'children', "siblings", 'spouse', 'other']
    color_dict = dict(zip(colors, labels))
    return colors, color_dict

def add_node(G, name):
    try:
        vertex = G.vs.find(name)
    except ValueError: # does not exist
        G.add_vertex(name)

def add_nodes_edges(G, first, sec):
    add_node(G, first)
    add_node(G, sec)
    G.vs.find(first)['label'] = first
    G.vs.find(sec)['label'] = sec

def get_top_20_by_edge_num(G):
    char_list = sorted(char_list, key=lambda x: x[1], reverse=True)[0:20]
    labels_list = [label for label, degree in char_list]
    delete_vertices = []
    for v in G.vs:
        if v['label'] not in labels_list:
            delete_vertices.append(v.index)
    G.delete_vertices(delete_vertices)

def build_network(triplets_path, filter_function):
    G = Graph()    
    triplets = read_triplets(triplets_path)
    for t in triplets:
        first, rel, sec = t.split(';')
        sec = sec.replace('\n', '')
        add_nodes_edges(G, first, sec)
        # Connection does not exist yet
        if not G.are_connected(first, sec):
            G.add_edge(first, sec, color=get_edge_color(rel))

    char_list = []
    for v in G.vs:
        label = v['label']
        char_list.append((label, v.degree()))

    # Filter nodes
    if filter_function != None:
        filter_function(G)
    return G

def visualize(out_fig_name, triplets_path, filter_function):
    G = build_network(triplets_path, filter_function)
    visual_style = {}

    # Define colors used for outdegree visualization
    colours = ['#fecc5c', '#a31a1c']

    # Set bbox and margin
    visual_style["bbox"] = (500,500)
    visual_style["margin"] = 70

    # Set vertex colours
    visual_style["vertex_color"] = 'grey'

    # Set vertex 
    visual_style["vertex_size"] = 20

    # Set vertex lable size
    visual_style["vertex_label_size"] = 8

    # Don't curve the edges
    visual_style["edge_curved"] = False

    visual_style["edge_color"] = G.es["color"]
    visual_style["vertex_spacing"] = 1000

    # Set the layout
    my_layout = G.layout_circle()
    # my_layout = G.layout_fruchterman_reingold()
    # my_layout = G.layout("kk", dim=2, spacing=100)
    # my_layout = G.layout_fruchterman_reingold(maxiter=1000, coolexp=0.5)
    visual_style["layout"] = my_layout

    colors, color_dict = get_color_dict()
    legend = [(color, color_dict[color]) for color in colors]
    plot(G, out_fig_name, **visual_style)

visualize('data/graph/graph.png', 'data/graph/tp_triplets.csv', None)