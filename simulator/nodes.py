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

        # TODO: Remove this debugging code once it's not needed
        print('node_id', self.node_id)
        print('')

        print('will_seize', self.will_seize)
        print('to_be_seized', self.to_be_seized)
        print('')

        print('will_delay', self.will_delay)
        print('delay', self.delay)
        print('')

        print('will_release', self.will_release)
        print('to_be_released', self.to_be_released)
        print('')

        self.statistics = {}

    def run(self, entity):
        """Perform the actions associated with this node."""
        arrival_time = self.env.now
        request = None

        if self.will_seize:
            # MVP Resource Seizing:
            # Resources must be seized and released in the same process or
            # they'll never be released. Resources are, at the moment, attached
            # to nodes (the process node) -- not to entities themselves.
            request = self.to_be_seized.request()
            yield request

        if self.will_delay:
            yield self.env.timeout(
                self.calculate_delay(self.delay['type'], **self.delay['args']))

        if self.will_release:
            # MVP Resource Seizing:
            # Resources must be seized and released in the same process or
            # they'll never be released. Resources are, at the moment, attached
            # to nodes (the process node) -- not to entities themselves.
            self.to_be_released.release(request)

        entity.record_statistic('arrive_and_depart', (arrival_time, self.env.now))
        self.proceed(self.outbound_edge, entity)

class Decision(Proceed, Statistics, SimNode, object):
    """A node which branches the simulation off in one of two directions based
    on some condition."""
    def __init__(self, env, node_id, branches):
        self.env = env
        self.node_id = node_id
        self.branches = branches

        self.statistics = {}

    def run(self, entity):
        """Perform the actions associated with this node."""
        # TODO
        pass

class Exit(Statistics, SimNode, object):
    """A node representing the end-of-the-line in a simulation."""
    def __init__(self, env, node_id):
        self.env = env
        self.node_id = node_id
        self.departed_entities = []

        self.statistics = {}

    def run(self, entity):
        """Perform the actions associated with this node."""
        entity.record_statistic('departure', (self.env.now))
        self.departed_entities.append(entity);

    def get_departed_entities(self):
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
