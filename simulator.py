from generators import *

# event types
ARRIVAL = 'A' # client arrives at the restaurant
# ENTRANCE = 'E' # client goes inside / is served
DEPARTURE = 'D' # client leaves the restaurant

# EVENT: (event_type, event_time)
EVENT_TYPE = 0
EVENT_TIME = 1

d = True # debug prints

"""
Main simulator function.
restaurant_capacity: how many people can be served at the same time
queue_capacity: how many people can wait in line at the same time
arrival_rate: average number of clients that arrive per time unit (lambda)
"""
def restaurant_simulator(restaurant_capacity = 30, queue_capacity = 15, arrival_rate = 0.5):
    current_time = 0
    max_time = 20 # simulation end condition
    events = [] # list of (event_type, event_time) tuples, sorted by event time
    serving = 0 # amount of people currently being served (serving <= restaurant_capacity)
    queue_size = 0 # amount of people currently waiting in line (queue_size <= queue_capacity)

    # interest measures
    arrival_count = 0 # clients who arrived
    entrance_count = 0 # clients who entered and were served
    departure_count = 0 # clients who were served and left
    drop_count = 0 # clients who left due to queue being full

    arrival_times = []
    entrance_times = []
    departure_times = []
    service_durations = []

    # Bootstrap
    events.append((ARRIVAL, current_time))

    # Simulator loop
    while len(events) > 0 and current_time < max_time:
        current_state = events.pop(0)

        # process arrival
        if current_state[EVENT_TYPE] == ARRIVAL:
            current_time = current_state[EVENT_TIME]
            arrival_count += 1

            if (d): print(f"A client arrives.")
            if (d): print(f"current time: {current_time}")
            if (d): print(f"arrival count: {arrival_count}")

            if serving < restaurant_capacity: # restaurant not full -> client is served
                if (d): print("Client will be served.")
                serving += 1
                if (d): print(f"clients inside: {serving}/{restaurant_capacity}")
                arrival_times.append(current_time)
                entrance_times.append(current_time) # client arrives and is served at the same time

                service_duration = exponential_generator(time.time()) # random variable X
                service_durations.append(service_duration)
                if (d): print(f"service duration: {service_duration}")
                events.append((DEPARTURE, current_time + service_duration))
                events = sorted(events, key = lambda e: e[EVENT_TIME])

            else: # restaurant full -> check if client can wait in line
                if (d): print("Restaurant is full.")
                if queue_size < queue_capacity: # queue not full -> client joins line
                    if (d): print("Client gets in line.")
                    queue_size += 1
                    if (d): print(f"queue size: {queue_size}/{queue_capacity}")
                    arrival_times.append(current_time)

                else: # queue full -> client leaves
                    if (d): print("Line is full. Client leaves.")
                    drop_count += 1
                    if (d): print(f"drop count: {drop_count}")

        # process departure
        elif current_state[EVENT_TYPE] == DEPARTURE:
            if (d): print("A client leaves the restaurant.")
            current_time = current_state[EVENT_TIME]
            serving -= 1
            departure_count += 1
            if (d): print(f"current time: {current_time}")
            if (d): print(f"clients inside: {serving}/{restaurant_capacity}")
            if (d): print(f"departure count: {departure_count}")

            if queue_size > 0: # line is not empty -> next client is served
                print("First client in line will be served.")
                queue_size -= 1
                serving += 1
                print(f"queue size: {queue_size}/{queue_capacity}")
                if (d): print(f"clients inside: {serving}/{restaurant_capacity}")

                service_duration = exponential_generator(time.time()) # random variable X
                service_durations.append(service_duration)
                if (d): print(f"service duration: {service_duration}")
                events.append((DEPARTURE, current_time + service_duration))
                events = sorted(events, key = lambda e: e[EVENT_TIME]) 

        # add next arrival
        time_until_next_arrival = exponential_generator(seed = time.time(), lambd = arrival_rate)
        if (d): print(f"time until next arrival: {time_until_next_arrival}")
        events.append((ARRIVAL, current_time + time_until_next_arrival))
        events = sorted(events, key = lambda e: e[EVENT_TIME])

    print("\n-- simulation over --\n")

    print("FINAL STATE:")
    print(f"line: {queue_size}/{queue_capacity}")
    print(f"restaurant: {serving}/{restaurant_capacity}")

    # Measures
    drop_rate = drop_count / arrival_count

    acc = 0
    for i in range(len(entrance_times)):
        waiting_time = entrance_times[i] - arrival_times[i]
        acc += waiting_time

    avg_waiting_time = acc / len(entrance_times)

    avg_service_time = sum(service_durations) / float(len(service_durations))

    print("\nMEASURES:")
    print(f"arrival count: {arrival_count}")
    print(f"departure count: {departure_count}")
    print(f"drop rate: {drop_rate}")
    print(f"average waiting time: {avg_waiting_time}")
    print(f"average service time: {avg_service_time}")


restaurant_simulator()