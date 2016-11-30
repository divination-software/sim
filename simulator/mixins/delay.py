"""Delay mixin"""
import random

class Delay(object):
    """Mixin which provides `calculate_delay`."""
    def calculate_delay(self, delay_type, **kwargs):
        """Delay the progress of the simulation"""
        duration = 0
        if delay_type == 'constant':
            duration = int(kwargs['val'])

        elif delay_type == 'uniform':
            duration = random.randint(
                int(kwargs['min']), int(kwargs['max']))

        elif delay_type == 'triangular':
            duration = random.triangular(
                int(kwargs['min']), int(kwargs['max']), int(kwargs['mid']))

        elif delay_type == 'exponential':
            duration = random.expovariate(
                int(kwargs['val']))

        return duration
