"""Define the nodes which make up a simulation"""
from copy import copy
from simulator.mixins.proceed import Proceed
from simulator.mixins.sim_node import SimNode
from simulator.mixins.statistics import Statistics


class Source(Proceed, Statistics, SimNode, object):
    """A node which generates instances of a Model which are moved through the
    simulation."""
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

            yield self.env.timeout(self.delay) # replace with delay_config

            self.created_count += 1


class Process(Proceed, Statistics, SimNode, object):
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

        # Override defaults
        if 'will_seize' in kwargs and kwargs['will_seize'] is True:
            self.will_seize = True
            # TODO: throw error if kwargs['to_be_seized'] isn't defined
            self.to_be_seized = kwargs['to_be_seized']

        if 'will_delay' in kwargs and kwargs['will_delay'] is True:
            self.will_delay = True
            # TODO: customize delay duration. Make it a generator?
            self.delay_duration = kwargs['delay_duration']

        if 'will_release' in kwargs and kwargs['will_release'] is True:
            self.will_release = True
            # TODO: throw error if kwargs['to_be_released'] isn't defined
            self.to_be_seized = kwargs['to_be_released']

    def run(self, instance):
        """Perform the actions associated with this node."""
        # print('%s is performing action at %7.4f!' % \
              # (instance.get_name(), self.env.now))
        arrival_time = self.env.now
        if self.will_seize:
            # TODO
            pass

        if self.will_delay:
            yield self.env.timeout(self.delay_duration)

        if self.will_release:
            # TODO
            pass

        # print('%s is done performing action at %7.4f!' % \
              # (instance.get_name(), self.env.now))
        self.record('arrive_and_depart', (arrival_time, self.env.now))
        self.proceed(self.outbound_edge, instance)


class Decision(Proceed, Statistics, SimNode, object):
    """A node which branches the simulation off in one or more directions based
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
    """A node representing the end-of-the-line in a simulation. This node also
    handles recording certain KPIs."""
    def __init__(self, env, node_id):
        self.env = env
        self.node_id = node_id

        self.statistics = {}

    def run(self, instance):
        """Perform the actions associated with this node."""
        self.record('departure', (self.env.now))

        # print('%s is exiting at %7.4f!' % \
              # (instance.get_name(), self.env.now))
