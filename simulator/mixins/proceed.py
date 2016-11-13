from ..nodes import Exit
from ..graph import get_node, get_edge

class Proceed(object):
    def proceed(self, edge, instance):
        print('Continuing along edge %s' % edge)
        target = get_edge(edge)['target']
        node = get_node(target)
        print(type(node).__name__)
        print(Exit.__name__)
        # if (type(node).__name__ == '')
        self.env.process(node.run(instance))
