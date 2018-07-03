import random

from generators import *

# event types
ARRIVAL = 'A'  # client arrives at the restaurant
DEPARTURE = 'D'  # client leaves the restaurant

# EVENT: (event_type, event_time)
EVENT_TYPE = 0
EVENT_TIME = 1

DEBUG = False  # debug prints

"""
Main simulator function.
restaurant_capacity: how many people can be served at the same time
queue_capacity: how many people can wait in queue at the same time
arrival_rate: average number of clients that arrive per time unit (lambda)
"""


def restaurant_simulator(simulation_time, arrival_rate, service_rate, queue_capacity=15):
    current_time = 0
    events = []  # list of (event_type, event_time) tuples, sorted by event time
    queue_size = 0  # amount of people currently waiting in queue (queue_size <= queue_capacity)

    # interest measures
    arrival_count = 0  # clients who arrived
    departure_count = 0  # clients who were served and left
    drop_count = 0  # clients who left due to queue being full

    arrival_times = []
    departure_times = []
    service_durations = []

    queue_sizes = []

    # Bootstrap
    events.append((ARRIVAL, current_time))

    # Simulator loop
    while current_time < simulation_time:
        current_state = events.pop(0)
        
        # Process arrival
        if current_state[EVENT_TYPE] == ARRIVAL:
            current_time = current_state[EVENT_TIME]
            arrival_count += 1

            if DEBUG: print(f"A client arrives.")
            if DEBUG: print(f"current time: {current_time}")
            if DEBUG: print(f"arrival count: {arrival_count}")

            # Queue not full -> client waits in queue
            if queue_size < queue_capacity:
                if DEBUG: print("Queue is not full. Client waits")
                arrival_times.append(current_time)
                queue_size += 1
                if DEBUG: print(f"queue size: {queue_size}")
            # Queue full -> client leaves
            else:
                if DEBUG: print("Queue is full. Client leaves.")
                drop_count += 1
                if DEBUG: print(f"drop count: {drop_count}")

            # Next arrival
            if DEBUG: print("Add next arrival.")
            time_until_next_arrival = exponential_generator(seed=random.randint(0, 9999999999999999999999), lambd=arrival_rate)  # X
            if DEBUG: print(f"time until next arrival: {time_until_next_arrival}")
            events.append((ARRIVAL, current_time + time_until_next_arrival))
            events = sorted(events, key = lambda e: e[EVENT_TIME])

            # Queue was empty
            if queue_size == 1:
                # Next departure
                if DEBUG: print("Add next departure.")
                service_duration = exponential_generator(seed=random.randint(0, 9999999999999999999999), lambd=service_rate)  # X
                service_durations.append(current_time)
                if DEBUG: print(f"service duration: {service_duration}")
                events.append((DEPARTURE, current_time + service_duration))
                events = sorted(events, key=lambda e: e[EVENT_TIME])

        # Process departure
        elif current_state[EVENT_TYPE] == DEPARTURE:
            if DEBUG: print("A client leaves the restaurant.")

            current_time = current_state[EVENT_TIME]
            departure_count += 1
            queue_size -= 1
            departure_times.append(current_time)

            if DEBUG: print(f"current time: {current_time}")
            if DEBUG: print(f"departure count: {departure_count}")

            # Queue is not empty -> add next departure
            if queue_size > 0:
                # Next departure
                service_duration = exponential_generator(seed=random.randint(0, 9999999999999999999999), lambd=service_rate)  # X
                service_durations.append(current_time)
                if DEBUG: print(f"service duration: {service_duration}")
                events.append((DEPARTURE, current_time + service_duration))
                events = sorted(events, key=lambda e: e[EVENT_TIME])

        queue_sizes.append(queue_size)

        if DEBUG: print()

    if DEBUG: print("\n-- Simulation is over --\n")

    if DEBUG: print("Final State:")
    if DEBUG: print(f"Queue: {queue_size}/{queue_capacity}")

    # Interest Measures

    # Utilization
    utilization = 0

    # Average queue size
    avg_queue_size = sum(queue_sizes) / float(len(queue_sizes))

    # Average requisition time
    avg_requisition_time = sum(service_durations) / simulation_time

    # Drop rate
    drop_rate = drop_count / arrival_count

    if (DEBUG): print("\nInterest Measures:")
    if (DEBUG): print(f"Arrival count: {arrival_count}")
    if (DEBUG): print(f"Departure count: {departure_count}")
    if (DEBUG): print(f"Drop count: {drop_count}")
    if (DEBUG): print(f"Drop rate: {drop_rate * 100}%")
    if (DEBUG): print(f"Average queue length: {sum(queue_sizes)/float(len(queue_sizes))}")

    return {"utilization": utilization, "avg_queue_size": avg_queue_size,
            "avg_requisition_time": avg_requisition_time, "drop_rate": drop_rate}


Ec = 0.110  # s -- esperança do tempo entre chegadas
Ex = 0.090  # s -- esperança do tempo para servir uma requisição

restaurant_simulator(simulation_time=3600, arrival_rate=float(1/Ec), service_rate=float(1/Ex))
