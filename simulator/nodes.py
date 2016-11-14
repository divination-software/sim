from copy import copy
# from simulator.mixins.proceed import Proceed
from simulator.graph import get_node, get_edge

class Proceed(object):
    def proceed(self, edge, instance):
        print('%s is continuing along edge %s' % \
              (instance.get_name(), edge))
        target = get_edge(edge)['target']
        node = get_node(target)
        if (type(node).__name__ == Exit.__name__):
            node.run(instance)
        else:
            self.env.process(node.run(instance))

class Source(Proceed, object):
    def __init__(self, env, Model, model_args, outbound_edge, delay):
        self.env = env
        self.Model = Model
        self.outbound_edge = outbound_edge
        self.delay = delay
        self.model_args = model_args

        self.created_count = 0

    def run(self):
        while True:
            print('Creating instance at %7.4f!' % self.env.now)

            modified_model_args = copy(self.model_args)
            modified_model_args['name'] = '%s %d' % \
                (self.model_args['name'], self.created_count)

            instance = self.Model(**modified_model_args)
            self.proceed(self.outbound_edge, instance)

            yield self.env.timeout(self.delay) # replace with delay_config

            self.created_count += 1


class Process(Proceed, object):
    def __init__(self, env, outbound_edge, **kwargs):
        self.env = env
        self.outbound_edge = outbound_edge
        # Set defaults
        self.will_seize = False
        self.will_delay = False
        self.will_release = False

        # Override defaults
        if 'will_seize' in kwargs and kwargs['will_seize'] is True:
            self.will_seize = True
            # TODO: throw error if kwargs['to_be_seized'] isn't defined
            self.to_be_seized = kwargs['to_be_seized']

        if 'will_delay' in kwargs and kwargs['will_delay'] is True:
            self.will_delay = True
            # TODO: customize delay duration. Make it a generator?
            self.delay_duration = 10

        if 'will_release' in kwargs and kwargs['will_release'] is True:
            self.will_release = True
            # TODO: throw error if kwargs['to_be_released'] isn't defined
            self.to_be_seized = kwargs['to_be_released']

    def run(self, instance):
        print('%s is performing action at %7.4f!' % \
              (instance.get_name(), self.env.now))
        if self.will_seize:
            # TODO
            pass

        if self.will_delay:
            self.env.timeout(self.delay_duration)

        if self.will_release:
            # TODO
            pass

        yield self.env.timeout(14)
        print('%s is done performing action at %7.4f!' % \
              (instance.get_name(), self.env.now))
        self.proceed(self.outbound_edge, instance)


class Decision(Proceed, object):
    def __init__(self, env, branches):
        self.env = env
        self.branches = branches

    def run(self, instance):
        for condition, edge in self.branches:
            if condition:
                self.proceed(edge, instance)


class Exit(object):
    def __init__(self, env):
        self.env = env
        pass

    def run(self, instance):
        # TODO: record statistics

        print('%s is exiting at %7.4f!' % \
              (instance.get_name(), self.env.now))
