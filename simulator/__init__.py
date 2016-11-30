"""Create and run a new simulation"""

import simpy
import logging
# import numpy as np
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
    """Representation of a runnable simulation."""
    def __init__(self, nodes, edges, resources):
        self.graph = {
            'nodes': nodes,
            'edges': edges,
            'resources': resources,
        }
        self.nodes = []
        self.node_statistics = {}

    def run(self):
        """Run the simulation and respond with statistics about the run."""
        for _ in range(3):
            self.nodes = []
            env = simpy.Environment()
            basic_args = {'name': 'Basic'}

            sources = []

            for node_id in self.graph['nodes']:
                node = None
                node_type = self.graph['nodes'][node_id]['type']
                # TODO: generalize the way configuration is passed into the node
                # constructors. Use kwargs and a config (dict) parameter?.
                if node_type == 'source':
                    node = Source(
                        env,
                        node_id,
                        Basic,
                        basic_args,
                        self.graph['nodes'][node_id]['outbound_edges'][0],
                        self.graph['nodes'][node_id]['metadata']['delay'])
                    sources.append(node)
                elif node_type == 'exit':
                    node = Exit(
                        env,
                        node_id)
                elif node_type == 'process':
                    node = Process(
                        env,
                        node_id,
                        self.graph['nodes'][node_id]['outbound_edges'][0],
                        process_type=self.graph['nodes'][node_id]['metadata']
                        ['processType'],
                        delay=self.graph['nodes'][node_id]['metadata']['delay'])

                add_node(node_id, node)
                self.nodes.append(node)

            for edge_id in self.graph['edges']:
                add_edge(edge_id, self.graph['edges'][edge_id])

            for source in sources:
                env.process(source.run())
            env.run(until=5000)

            for node in self.nodes:
                if node.get_node_id() not in self.node_statistics:
                    self.node_statistics[node.get_node_id()] = {
                        'node_type': node.get_node_type(),
                        'statistics': [node.get_statistics()]}
                else:
                    self.node_statistics[node.get_node_id()]['statistics'].append(
                            node.get_statistics())

        return self.node_statistics

'''
        for node_id in self.node_statistics:
            if self.node_statistics[node_id]['node_type'] == 'Source':
                for run in self.node_statistics[node_id]['statistics']:
                    created_at_times = np.array(run)
                    print(np.diff(created_at_times))
'''


