"""Random"""
import random
"""Define the nodes which make up a simulation"""
from simulator.mixins.delay import Delay
from simulator.mixins.proceed import Proceed
from simulator.mixins.sim_node import SimNode
from simulator.mixins.statistics import Statistics

class Source(Proceed, Delay, Statistics, SimNode, object):
    """Generates entities, at some interval, which move through the simulation.
    These entities represent various actors as defined by the user when they
    build the simulation."""
    def __init__(self, env, node_id, Model, model_args, outbound_edge, delay):
        self.env = env
        self.node_id = node_id
        self.Model = Model
        self.outbound_edge = outbound_edge
        self.delay = delay
        self.model_args = model_args

        self.created_count = 0

        self.statistics = {}

    def run(self):
        """Perform the actions associated with this node."""
        while True:
            # Create entity which will move through the simulation
            entity = self.Model(self.created_count)

            entity.record_statistic('created_at', self.env.now)
            entity.record_statistic('created_by', self.node_id)

            self.proceed(self.outbound_edge, entity)

            # Delay before creating another entity
            yield self.env.timeout(
                self.calculate_delay(self.delay['type'], **self.delay['args']))
            self.created_count += 1

class Process(Proceed, Delay, Statistics, SimNode, object):
    """A node which performs a combination of seizing, delaying, and releasing.

    Seizing:
        Claim a some quantity of a resource for the current entity

    Delay:
        Delay the progress of an entity through the simulation

    Release:
        Renounce the current entity's claim on some quantity of a resource
    """
    def __init__(self, env, node_id, outbound_edge, **kwargs):
        self.env = env
        self.node_id = node_id
        self.outbound_edge = outbound_edge

        self.will_seize = kwargs['will_seize']
        self.to_be_seized = kwargs['to_be_seized']

        self.will_delay = kwargs['will_delay']
        self.delay = kwargs['delay']

        self.will_release = kwargs['will_release']
        self.to_be_released = kwargs['to_be_released']

        self.statistics = {}

    def run(self, entity):
        """Perform the actions associated with this node."""
        entity.record_statistic('visited', self.node_id)
        arrival_time = self.env.now

        request = None

        if self.will_seize:
            request = self.to_be_seized.request()
            yield request
            entity.hold_resource(self.to_be_seized, request)

        if self.will_delay:
            yield self.env.timeout(
                self.calculate_delay(self.delay['type'], **self.delay['args']))

        if self.will_release:
            entity.release_resource(self.to_be_released)

        entity.record_statistic('process_visits', {
            'node_id': self.node_id,
            'arrived_at': arrival_time,
            'departed_at': self.env.now
        })

        self.proceed(self.outbound_edge, entity)

class Decision(Proceed, Statistics, SimNode, object):
    """A node which branches the simulation off in one of two directions based
    on some condition."""
    def __init__(self, env, node_id, branches, probability):
        self.env = env
        self.node_id = node_id
        self.branches = branches
        self.probability = probability
        self.statistics = {}

    def run(self, entity):
        """Perform the actions associated with this node."""
        entity.record_statistic('visited', self.node_id)

        if random.uniform(0, 1) > self.probability:
            self.proceed(self.branches['up'], entity)
        else:
            self.proceed(self.branches['down'], entity)

class Exit(Statistics, SimNode, object):
    """A node representing the end-of-the-line in a simulation."""
    def __init__(self, env, node_id):
        self.env = env
        self.node_id = node_id
        self.departed_entities = []

        self.statistics = {}

    def run(self, entity):
        """Perform the actions associated with this node."""
        entity.record_statistic('departed_at', self.env.now)
        entity.record_statistic('departed_through', self.node_id)
        self.departed_entities.append(entity)

    def get_departed_entities(self):
        """Get departed from entities"""
        return self.departed_entities

class Spread(Proceed, Statistics, SimNode, object):
    """Not implemented yet."""
    def __init__(self, env, node_id, branches):
        pass

    def run(self, entity):
        """Not implemented yet."""
        pass

class Modify(Proceed, Statistics, SimNode, object):
    """Not implemented yet."""
    def __init__(self, env, node_id, branches):
        pass

    def run(self, entity):
        """Not implemented yet."""
        pass

class Record(Proceed, Statistics, SimNode, object):
    """Not implemented yet."""
    def __init__(self, env, node_id, branches):
        pass

    def run(self, entity):
        """Not implemented yet."""
        pass
