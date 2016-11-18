"""Proceed mixin"""
from simulator.graph import get_node, get_edge

class Proceed(object):
    """Mixin which provides `proceed`."""
    def proceed(self, edge, instance):
        """Move the simulation along to the next node."""
        #print('%s is continuing along edge %s' % \
              #(instance.get_name(), edge))
        target = get_edge(edge)['target']
        node = get_node(target)
        if type(node).__name__ == 'Exit':
            node.run(instance)
        else:
            self.env.process(node.run(instance))
