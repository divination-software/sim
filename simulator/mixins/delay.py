"""Delay mixin"""
import random

class Delay(object):
    """Mixin which provides `calculate_delay`."""
    def calculate_delay(self, delayType, **kwargs):
        """Delay the progress of the simulation"""
        duration = 0
        if delayType == 'constant':
            duration = int(kwargs['val'])

        elif delayType == 'uniform':
            duration = random.randint(
                int(kwargs['min']), int(kwargs['max']))

        elif delayType == 'triangular':
            duration = random.triangular(
                int(kwargs['min']), int(kwargs['max']), int(kwargs['mid']))

        elif delayType == 'exponential':
            duration = random.expovariate(
                int(kwargs['val']))

        return duration
