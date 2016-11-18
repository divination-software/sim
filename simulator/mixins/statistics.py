"""Statistics mixin"""

class Statistics(object):
    """Mixin providing statistics recording capabilities to simulation nodes."""

    def record(self, event, record):
        """Record a stat."""
        if event not in self.statistics:
            self.statistics[event] = [record]
        else:
            self.statistics[event].append(record)

    def get_statistics(self):
        """Get all statistics for this node."""
        return self.statistics
