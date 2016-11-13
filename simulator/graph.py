EDGES = {}
NODES = {}

def add_node(key, value):
    NODES[key] = value

def add_edge(key, value):
    EDGES[key] = value

def get_node(key):
    return NODES[key]

def get_edge(key):
    return EDGES[key]
