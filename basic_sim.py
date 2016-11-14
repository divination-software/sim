import simpy
from simulator.nodes import Source, Process, Exit
from simulator.graph import add_node, add_edge

class Basic(object):
    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs['name']

    def get_name(self):
        return self.name

if __name__ == '__main__':
    env = simpy.Environment()
    basic_args = {'name': 'Basic'}

    EDGES = {
        '0': {'source': '2', 'target': '3'},
        '1': {'source': '3', 'target': '4'},
    }
    for key in EDGES:
        add_edge(key, EDGES[key])

    NODES = {
        '2': Source(env, Basic, basic_args, '0', 10),
        '3': Process(env, '1'),
        '4': Exit(env),
    }
    for key in NODES:
        add_node(key, NODES[key])


    env.process(NODES['2'].run())
    env.run(until=50)
