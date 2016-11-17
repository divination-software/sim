"""Create and run a new simulation"""

import simpy
from .nodes import Source, Process, Exit
from .graph import add_node, add_edge, get_nodes, get_edges

class Basic(object):
    """Simple class to pass through the simulation (as instance)."""
    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs['name']

    def get_name(self):
        """Return the instance's name."""
        return self.name

class Simulation(object):
    """Construct and run a simulation."""
    def __init__(self, nodes, edges):
        env = simpy.Environment()
        basic_args = {'name': 'Basic'}

        sources = []

        for node_id in nodes:
            node = None
            node_type = nodes[node_id]['type']
            # TODO: generalize the way configuration is passed into the node
            # constructors. Use kwargs and a config (dict) parameter?.
            if node_type == 'source':
                node = Source(
                    env,
                    Basic,
                    basic_args,
                    nodes[node_id]['outbound_edges'][0],
                    int(nodes[node_id]['Delay']))
                sources.append(node)
            elif node_type == 'exit':
                node = Exit(env)
            elif node_type == 'process':
                node = Process(
                    env,
                    nodes[node_id]['outbound_edges'][0],
                    will_delay=True,
                    delay_duration=int(nodes[node_id]['Delay']))

            add_node(node_id, node)

        for edge_id in edges:
            add_edge(edge_id, edges[edge_id])

        for source in sources:
            env.process(source.run())
        env.run(until=50)
