"""Delay mixin"""
import random

class Delay(object):
    """Mixin which provides `calculate_delay`."""
    def calculate_delay(self, delayType, **kwargs):
        """Delay the progress of the simulation"""
        duration = 0
        if delayType == 'constant':
            duration = kwargs['value']

        elif delayType == 'uniform':
            duration = random.randint(
                kwargs['min'], kwargs['max'])

        elif delayType == 'triangular':
            duration = random.triangular(
                kwargs['min'], kwargs['max'], kwargs['mode'])

        elif delayType == 'exponential':
            duration = random.expovariate(
                kwargs['value'])

        return duration
