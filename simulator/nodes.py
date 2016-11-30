"""Define the nodes which make up a simulation"""
from copy import copy
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
            # print('Creating instance at %7.4f!' % self.env.now)
            self.record('created_at', self.env.now)

            modified_model_args = copy(self.model_args)
            modified_model_args['name'] = '%s %d' % \
                (self.model_args['name'], self.created_count)

            instance = self.Model(**modified_model_args)
            self.proceed(self.outbound_edge, instance)

            yield self.env.timeout(
                self.calculate_delay(self.delay['type'], **self.delay['args']))

            self.created_count += 1

class Process(Proceed, Delay, Statistics, SimNode, object):
    """A node which performs a combination of seizing, delaying, and releasing.

    Seizing:
        Claim a some quantity of a resource for the current instance

    Delay:
        Delay the progress of an instance through the simulation

    Release:
        Renounce the current instance's claim on some quantity of a resource
    """
    def __init__(self, env, node_id, outbound_edge, **kwargs):
        self.env = env
        self.node_id = node_id
        self.outbound_edge = outbound_edge

        # Set defaults
        self.will_seize = False
        self.will_delay = False
        self.will_release = False

        self.statistics = {}

        process_type = kwargs['process_type']
        self.delay = kwargs['delay']
        if process_type == 'delay':
            self.will_delay = True
        elif process_type == 'siezeDelay':
            self.will_seize = True
            self.will_delay = True
        elif process_type == 'sieze':
            self.will_seize = True
        elif process_type == 'siezeDelayRelease':
            self.will_delay = True
            self.will_release = True
            self.will_seize = True

        # # Override defaults
        # if 'will_seize' in kwargs and kwargs['will_seize'] is True:
        #     self.will_seize = True
        #     # TODO: throw error if kwargs['to_be_seized'] isn't defined
        #     self.to_be_seized = kwargs['to_be_seized']

        # if 'will_delay' in kwargs and kwargs['will_delay'] is True:
        #     self.will_delay = True
        #     self.delay = kwargs['delay']

        # if 'will_release' in kwargs and kwargs['will_release'] is True:
        #     self.will_release = True
        #     # TODO: throw error if kwargs['to_be_released'] isn't defined
        #     self.to_be_seized = kwargs['to_be_released']

    def run(self, instance):
        """Perform the actions associated with this node."""
        # print('%s is performing action at %7.4f!' % \
              # (instance.get_name(), self.env.now))
        arrival_time = self.env.now
        if self.will_seize:
            # TODO
            pass

        if self.will_delay:
            yield self.env.timeout(
                self.calculate_delay(self.delay['type'], **self.delay['args']))

        if self.will_release:
            # TODO
            pass

        # print('%s is done performing action at %7.4f!' % \
              # (instance.get_name(), self.env.now))
        self.record('arrive_and_depart', (arrival_time, self.env.now))
        self.proceed(self.outbound_edge, instance)

class Decision(Proceed, Statistics, SimNode, object):
    """A node which branches the simulation off in one of two directions based
    on some condition."""
    def __init__(self, env, node_id, branches):
        self.env = env
        self.node_id = node_id
        self.branches = branches

        self.statistics = {}

    def run(self, instance):
        """Perform the actions associated with this node."""
        # TODO
        pass

class Exit(Statistics, SimNode, object):
    """A node representing the end-of-the-line in a simulation."""
    def __init__(self, env, node_id):
        self.env = env
        self.node_id = node_id

        self.statistics = {}

    def run(self, instance):
        """Perform the actions associated with this node."""
        self.record('departure', (self.env.now))

        # print('%s is exiting at %7.4f!' % \
              # (instance.get_name(), self.env.now))

class Spread(Proceed, Statistics, SimNode, object):
    """Not implemented yet."""
    def __init__(self, env, node_id, branches):
        pass

    def run(self, instance):
        """Not implemented yet."""
        pass

class Modify(Proceed, Statistics, SimNode, object):
    """Not implemented yet."""
    def __init__(self, env, node_id, branches):
        pass

    def run(self, instance):
        """Not implemented yet."""
        pass

class Record(Proceed, Statistics, SimNode, object):
    """Not implemented yet."""
    def __init__(self, env, node_id, branches):
        pass

    def run(self, instance):
        """Not implemented yet."""
        pass
