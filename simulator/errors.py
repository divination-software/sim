"""Custom errors related to simulations"""

class SimBuildError(Exception):
    """Exception indicating the simulation couldn't be parsed."""
    def __init__(self, message, node_type=None, node_id=None):
        super(SimBuildError, self).__init__(message)
        self.message = message
        self.node_type = node_type
        self.node_id = node_id
