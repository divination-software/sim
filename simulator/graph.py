"""Store a globally accessible record of nodes and edges"""

EDGES = {}
NODES = {}

def add_node(key, value):
    """Add a single key-value pair to NODES."""
    NODES[key] = value

def add_edge(key, value):
    """Add a single key-value pair to EDGES."""
    EDGES[key] = value

def get_node(key):
    """Retrieve a single node."""
    return NODES[key]

def get_edge(key):
    """Retrieve a single edge."""
    return EDGES[key]

def get_nodes():
    """Retrieve all nodes."""
    return NODES

def get_edges():
    """Retrieve all edges."""
    return EDGES
