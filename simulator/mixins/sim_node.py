"""SimNode mixin"""

class SimNode(object):
    """Mixin to expose some data about the node in the simulation."""

    def get_node_id(self):
        """Return the node's id."""
        return self.node_id

    def get_node_type(self):
        """Return the class name for this node."""
        return self.__class__.__name__
