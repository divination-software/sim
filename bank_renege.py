"""
Bank renege example

Covers:

- Resources: Resource
- Condition events

Scenario:
  A counter with a random service time and customers who renege. Based on the
  program bank08.py from TheBank tutorial of SimPy 2. (KGM)

"""
import random

import simpy


RANDOM_SEED = 42
NEW_CUSTOMERS = 5  # Total number of customers
INTERVAL_CUSTOMERS = 10.0  # Generate new customers roughly every x seconds
MIN_PATIENCE = 1  # Min. customer patience
MAX_PATIENCE = 300  # Max. customer patience


def talk_with_teller(env, name, counter, time_in_bank):
    print('%7.4f %s: Arrived and is waiting to talk with the teller' % (env.now, name))
    # seize
    request = counter.request()
    yield request
    print('%7.4f %s: Talking with the teller' % (env.now, name))

    # delay
    yield env.timeout(time_in_bank)

    # counter.release(request)

    # next(...)
    print('%7.4f %s: Finished talking with the teller' % (env.now, name))
    env.process(fill_out_form(env, name, counter, time_in_bank, request))

def fill_out_form(env, name, counter, time_in_bank, request):
    print('%7.4f %s: Starting to fill out the form' % (env.now, name))
    # delay
    yield env.timeout(15)

    print('%7.4f %s: Finished filling out the form' % (env.now, name))
    # release
    counter.release(request)

    print('%7.4f %s: Finished' % (env.now, name))


def source(env, number, interval, counter):
    """Source generates customers randomly"""
    for i in range(number):
        w = talk_with_teller(env, 'Customer%02d' % i, counter, time_in_bank=12.0)
        env.process(w)
        # c = customer(env, 'Customer%02d' % i, counter, time_in_bank=12.0)
        # env.process(c)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)


def customer(env, name, counter, time_in_bank):
    """Customer arrives, is served and leaves."""
    print('%7.4f %s: Here I am' % (env.now, name))

    # next(...)
    env.process(talk_with_teller(env, name, counter, time_in_bank))

"""
    with counter.request() as req:
        patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
        # Wait for the counter or abort at the end of our tether
        results = yield req | env.timeout(patience)

        wait = env.now - arrive

        if req in results:
            # We got to the counter
            print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))

            tib = random.expovariate(1.0 / time_in_bank)
            yield env.timeout(tib)
            print('%7.4f %s: Finished' % (env.now, name))

        else:
            # We reneged
            print('%7.4f %s: RENEGED after %6.3f' % (env.now, name, wait))
"""
# Setup and start the simulation
print('Bank renege')
random.seed(RANDOM_SEED)
env = simpy.Environment()

# Start processes and run
counter = simpy.Resource(env, capacity=2)
env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
env.run()
