from generators import *

DEBUG = True

# Event types
ARRIVAL = 'A'  # client arrives at the restaurant
# ENTRANCE = 'E' # client goes inside / is served
DEPARTURE = 'D'  # client leaves the restaurant

# EVENT: (event_type, event_time)
EVENT_TYPE = 0
EVENT_TIME = 1

"""
Main simulator function.
restaurant_capacity: how many people can be served at the same time
queue_capacity: how many people can wait in line at the same time
arrival_rate: average number of clients that arrive per time unit (lambda)
"""


def restaurant_simulator(restaurant_capacity=30, queue_capacity=15, arrival_rate=0.2):
    current_time = 0
    max_time = 1  # simulation end condition
    events = []  # list of (event_type, event_time) tuples, sorted by event time
    serving = 0  # amount of people currently being served (serving <= restaurant_capacity)
    queue_size = 0  # amount of people currently waiting in line (queue_size <= queue_capacity)

    # Interest measures
    arrival_count = 0
    departure_count = 0
    drop_count = 0  # amount of events dropped due to queue being full

    arrival_times = []
    entrance_times = []
    departure_times = []

    # Bootstrap
    events.append((ARRIVAL, current_time))

    # Simulator loop
    # while len(events) > 0 and current_time < max_time:
    while len(events) > 0 and arrival_count < 1000:
        if DEBUG: print(events)

        current_state = events.pop(0)

        # Process arrival
        if current_state[EVENT_TYPE] == ARRIVAL:
            current_time = current_state[EVENT_TIME]
            arrival_count += 1

            # Restaurant not full -> client is served
            if serving < restaurant_capacity:
                serving += 1
                arrival_times.append(current_time)
                entrance_times.append(current_time)  # client arrives and is served at the same time

                # Next departure
                service_duration = exponential_generator(time.time())  # random variable X
                events.append((DEPARTURE, current_time + service_duration))
                events = sorted(events, key=lambda e: e[EVENT_TIME])
            # Restaurant full -> check if client can wait in line
            else:
                # Queue not full -> client joins line
                if queue_size < queue_capacity:
                    queue_size += 1
                    arrival_times.append(current_time)
                # Queue full -> client leaves
                else:
                    drop_count += 1
        # Process departure
        elif current_state[EVENT_TYPE] == DEPARTURE:
            current_time = current_state[EVENT_TIME]
            serving -= 1
            departure_count += 1

            # Line is not empty -> next client is served
            if queue_size > 0:
                queue_size -= 1
                serving += 1

                # Next departure
                service_duration = exponential_generator(time.time())  # Random variable X
                events.append((DEPARTURE, current_time + service_duration))
                events = sorted(events, key=lambda e: e[EVENT_TIME])

        # Add next arrival
        time_until_next_arrival = exponential_generator(time.time(), lambd=arrival_rate)
        events.append((ARRIVAL, current_time + time_until_next_arrival))
        events = sorted(events, key=lambda e: e[EVENT_TIME])

    #  Measures
    drop_rate = drop_count / arrival_count

    """
    ac = 0
    for i in range(len(arrival_times)):
        waiting_time = departure_times[i] - arrival_times[i]
        ac += waiting_time
    
    avg_waiting_time = ac / len(arrival_times)
    """

    if DEBUG: print("Interest Measures:")
    if DEBUG: print(f"arrival count: {arrival_count}")
    if DEBUG: print(f"departure count: {departure_count}")
    if DEBUG: print(f"drop rate: {drop_rate}")
    if DEBUG: print(f"drops: {drop_count}")
    if DEBUG: print(f"serving: {serving}")
    if DEBUG: print(f"queue size: {queue_size}")
    # print(f"average waiting time: {avg_waiting_time}")


restaurant_simulator()