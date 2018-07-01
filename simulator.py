from generators import *

ARRIVAL = 'A'
DEPARTURE = 'D'

# EVENT: [event_type, event_time]
EVENT_TYPE = 0
EVENT_TIME = 1

def get_event_time(event):
    return event[1]


def simulator():
    current_time = 0
    max_time = 10000 # Simulation end condition
    events = []

    # Interest measures
    arrival_count = 0 # total of arrivals
    departure_count = 0 # total of departures
    queue_size = 0 # current queue size
    queue_capacity = 15 # maximum queue size acceptable before starting to drop events
    drop_count = 0 # amount of dropped events

    arrival_times = []
    departure_times = []

    # Bootstrap
    events.append([ARRIVAL, current_time])

    # Simulator loop
    while len(events) > 0 and current_time < max_time:
        print(events)

        current_state = events.pop(0)

        if current_state[EVENT_TYPE] == ARRIVAL:
            current_time = current_state[EVENT_TIME]
            arrival_count += 1

            if queue_size == queue_capacity:
                # Queue full -> drop event
                drop_count += 1

            else:
                queue_size += 1
                print(f"queue size: {queue_size}")
                arrival_times.append(current_time)

            # Time until next arrival
            seed = time.clock() * pow(10, 20)
            next_arrival = int(linear_congruential_generator(seed)[0] * 100)
            events.append([ARRIVAL, current_time + next_arrival])
            events = sorted(events, key = lambda x: x[EVENT_TIME])

            if queue_size == 1:  # Queue was empty
                # Time until next departure
                seed = time.clock() * pow(10, 20)
                next_departure = int(linear_congruential_generator(seed)[0] * 100)
                events.append([DEPARTURE, current_time + next_departure])
                events = sorted(events, key = lambda x: x[EVENT_TIME])


        elif current_state[EVENT_TYPE] == DEPARTURE:
            current_time = current_state[EVENT_TIME]
            queue_size -= 1
            print(f"queue size: {queue_size}")
            departure_count += 1

            departure_times.append(current_time)

            if queue_size > 0:  # Queue is not empty
                # Time until next departure
                seed = time.clock() * pow(10, 20)
                next_departure = int(linear_congruential_generator(seed)[0] * 100)
                events.append([DEPARTURE, current_time + next_departure])

    # Measures
    drop_rate = drop_count / arrival_count

    """
    ac = 0
    for i in range(len(arrival_times)):
        waiting_time = departure_times[i] - arrival_times[i]
        ac += waiting_time
    
    avg_waiting_time = ac / len(arrival_times)
    """
    # TODO: algo errado, tem mais arrival_times do que departure_times

    print(f"arrival count: {arrival_count}")
    print(f"departure count: {departure_count}")
    print(f"drop rate: {drop_rate}")
    # print(f"average waiting time: {avg_waiting_time}")


simulator()