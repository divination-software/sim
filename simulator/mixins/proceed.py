from simulator.nodes import Exit
from simulator.graph import get_node, get_edge

class Proceed(object):
    def proceed(self, edge, instance):
        print('%s is continuing along edge %d' % \
              (instance.get_name(), edge))
        target = get_edge(edge)['target']
        node = get_node(target)
        print(type(node).__name__)
        print(Exit.__name__)
        # if (type(node).__name__ == '')
        self.env.process(node.run(instance))
