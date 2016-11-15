import simpy
from simulator.nodes import Source, Process, Exit
from simulator.graph import add_node, add_edge

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
    def __init__(self, simulation_xml):
        env = simpy.Environment()
        basic_args = {'name': 'Basic'}

        edges = {
            '0': {'source': '2', 'target': '3'},
            '1': {'source': '3', 'target': '4'},
        }
        for key in edges:
            add_edge(key, edges[key])

        nodes = {
            '2': Source(env, Basic, basic_args, '0', 10),
            '3': Process(env, '1', will_delay=True, delay_duration=50),
            '4': Exit(env),
        }
        for key in nodes:
            add_node(key, nodes[key])


        env.process(nodes['2'].run())
        env.run(until=50)
