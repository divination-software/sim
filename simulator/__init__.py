"""Create and run a new simulation"""

import simpy
# import logging
# import numpy as np
from .nodes import Source, Process, Exit, Decision
from .graph import add_node, add_edge

class Basic(object):
    """Simple class to pass through the simulation (as instance)."""
    def __init__(self, entity_id):
        self.statistics = {}
        self.id = entity_id
        self.resources = {}

    def get_name(self):
        """Return the instance's name."""
        return self.name

    def record_statistic(self, event, record):
        """Record a stat."""
        if event not in self.statistics:
            self.statistics[event] = [record]
        else:
            self.statistics[event].append(record)

    def get_statistics(self):
        """Get all statistics for this node."""
        return self.statistics

    def hold_resource(self, resource, request):
        self.resources[resource] = request

    def release_resource(self, resource):
        resource.release(self.resources[resource])
        del self.resources[resource]

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
        for _ in range(1):
            self.nodes = []
            env = simpy.Environment()
            basic_args = {'name': 'Basic'}

            # Build array of simpy Resource objects for use later
            resources = {}
            for resource_id in self.graph['resources']:
                resource_name = self.graph['resources'][resource_id]['name']
                resource_count = 1
                try:
                    resource_count = int(self.graph['resources'][resource_id]['count'])
                except ValueError:
                    # Use default value of 1
                    pass

                resources[resource_name] = simpy.Resource(env, capacity=resource_count)

            sources = []
            exits = []

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
                    exits.append(node)
                elif node_type == 'decision':
                    # get branches for this current decision
                    branches = {}
                    edges = []
                    for edge_id in self.graph['edges']:
                        branch = self.graph['edges'][edge_id]
                        branch_id = branch['source']
                        if branch_id == node_id:
                            edges.append(edge_id)

                    if len(edges) == 2:
                        branches['up'] = edges[0]
                        branches['down'] = edges[1]

                    # Get the metadata to grab the probability value
                    metadata = self.graph['nodes'][node_id]['metadata']
                    # probability value is float type
                    probability = float(metadata['args']['probability'])
                    node = Decision(env, node_id, branches, probability)
                elif node_type == 'process':
                    process_type = self.graph['nodes'][node_id] \
                        ['metadata']['processType']
                    delay = self.graph['nodes'][node_id]['metadata']['delay']

                    # Set defaults
                    will_delay = False
                    will_seize = False
                    will_release = False
                    to_be_seized = None
                    to_be_released = None

                    # Override defaults
                    if process_type == 'delay':
                        will_delay = True
                    elif process_type == 'siezeDelay':
                        will_seize = True
                        will_delay = True
                    elif process_type == 'sieze':
                        will_seize = True
                    elif process_type == 'siezeDelayRelease':
                        will_delay = True
                        will_release = True
                        will_seize = True

                    # If we're seizing or releasing we need to know about the
                    # resource specified for this process.
                    if will_seize or will_release:
                        process_resource_name = delay['args']['resource']
                        if will_seize:
                            to_be_seized = resources[process_resource_name]
                        if will_release:
                            to_be_released = resources[process_resource_name]

                    node = Process(
                        env,
                        node_id,
                        self.graph['nodes'][node_id]['outbound_edges'][0],
                        will_seize=will_seize,
                        to_be_seized=to_be_seized,
                        will_delay=will_delay,
                        delay=delay,
                        will_release=will_release,
                        to_be_released=to_be_released)

                add_node(node_id, node)
                self.nodes.append(node)

            for edge_id in self.graph['edges']:
                add_edge(edge_id, self.graph['edges'][edge_id])

            for source in sources:
                env.process(source.run())

            days_to_run = 1
            hours_in_a_day = 8
            seconds_in_a_day = 60 * 60 * hours_in_a_day
            simulation_duration = days_to_run * seconds_in_a_day
            env.run(until=simulation_duration)

            for node in self.nodes:
                if node.get_node_id() not in self.node_statistics:
                    self.node_statistics[node.get_node_id()] = {
                        'node_type': node.get_node_type(),
                        'statistics': [node.get_statistics()]}
                else:
                    self.node_statistics[node.get_node_id()]['statistics'].append(
                            node.get_statistics())

            departed_entities = []
            for exit in exits:
                departed_entities.extend(exit.get_departed_entities())

            for entity in departed_entities:
                statistics = entity.get_statistics()
                # TODO: Generate actual statistics
                # TODO: The return value of this method should be those newly
                # generated statistics
                print(statistics)

        return self.node_statistics
