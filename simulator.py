from generators import *

# event types
ARRIVAL = 'A' # client arrives at the restaurant
DEPARTURE = 'D' # client leaves the restaurant

# EVENT: (event_type, event_time)
EVENT_TYPE = 0
EVENT_TIME = 1

DEBUG = False  # debug prints

"""
Main simulator function.
restaurant_capacity: how many people can be served at the same time
queue_capacity: how many people can wait in line at the same time
arrival_rate: average number of clients that arrive per time unit (lambda)
"""

def restaurant_simulator(simulation_time, arrival_rate, service_rate):
    current_time = 0
    events = []  # list of (event_type, event_time) tuples, sorted by event time
    # serving = 0  # amount of people currently being served (serving <= restaurant_capacity)
    restaurant_capacity = 30
    queue_size = 0  # amount of people currently waiting in line (queue_size <= queue_capacity)
    queue_capacity = 15

    # interest measures
    arrival_count = 0  # clients who arrived
    departure_count = 0  # clients who were served and left
    drop_count = 0  # clients who left due to queue being full

    arrival_times = []
    entrance_times = []
    # arrival_times[i] and entrance_times[i] refer to the same event
    departure_times = [] # useless?
    service_durations = []

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
            
            if queue_size < queue_capacity: # Queue not full -> client waits in line
                arrival_times.append(current_time)
                queue_size += 1
                if DEBUG: print(f"queue size: {queue_size}")

            else: # Queue full -> client leaves
                if DEBUG: print("Line is full. Client leaves.")
                drop_count += 1
                if DEBUG: print(f"drop count: {drop_count}")

            # Next arrival
            if DEBUG: print("Add next arrival.")
            time_until_next_arrival = exponential_generator(seed = time.time(), lambd = arrival_rate) # X
            if DEBUG: print(f"time until next arrival: {time_until_next_arrival}")
            events.append((ARRIVAL, current_time + time_until_next_arrival))
            events = sorted(events, key = lambda e: e[EVENT_TIME])
            

            if queue_size == 1: # Queue was empty
                if DEBUG: print("Add next departure.")
                service_duration = exponential_generator(seed = time.time(), lambd = service_rate) # X
                service_durations.append(current_time)
                if DEBUG: print(f"service duration: {service_duration}")
                events.append((DEPARTURE, current_time + service_duration))
                events = sorted(events, key = lambda e: e[EVENT_TIME])


        # Process departure
        elif current_state[EVENT_TYPE] == DEPARTURE:
            if DEBUG: print("A client leaves the restaurant.")

            current_time = current_state[EVENT_TIME]
            departure_count += 1
            queue_size -= 1

            if DEBUG: print(f"current time: {current_time}")
            if DEBUG: print(f"departure count: {departure_count}")

            if (queue_size > 0): # Queue is not empty -> add next departure
                service_duration = exponential_generator(seed = time.time(), lambd = service_rate) # X
                service_durations.append(current_time)
                if DEBUG: print(f"service duration: {service_duration}")
                events.append((DEPARTURE, current_time + service_duration))
                events = sorted(events, key = lambda e: e[EVENT_TIME])
                
        if DEBUG: print()
    

    print("\n-- simulation over --\n")

    print("FINAL STATE:")
    print(f"line: {queue_size}/{queue_capacity}")

    #  Measures
    drop_rate = drop_count / arrival_count

    """
    acc = 0
    for i in range(len(entrance_times)):
        waiting_time = entrance_times[i] - arrival_times[i]
        acc += waiting_time

    avg_waiting_time = acc / len(entrance_times)
    """
    avg_service_time = sum(service_durations) / float(len(service_durations))

    print("\nMEASURES:")
    print(f"arrival count: {arrival_count}")
    print(f"departure count: {departure_count}")
    print(f"drop count: {drop_count}")
    print(f"drop rate: {drop_rate}")
    # print(f"average waiting time: {avg_waiting_time}")
    # print(f"average service time: {avg_service_time}")


Ec = 0.110 # s -- esperança do tempo entre chegadas
Ex = 0.090 # s -- esperança do tempo para servir uma requisição

restaurant_simulator(simulation_time = 3600, arrival_rate = float(1/Ec), service_rate = float(1/Ex))