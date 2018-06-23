import random

ARRIVAL = 0
DEPARTURE = 1

EVENT_TYPE = 0
EVENT_TIME = 1


def toll():
    current_time = 0

    # Bootstrap
    events = [[ARRIVAL, current_time]]

    # Interest measures
    queue_count = 0
    arrivals_count = 0
    departures_count = 0

    arrival_times = []
    departure_times = []

    # Simulator loop
    while len(events) > 0:
        print(events)
        current_state = events.pop(0)

        if current_state[EVENT_TYPE] == ARRIVAL:
            current_time = current_state[EVENT_TIME]
            queue_count += 1
            arrivals_count += 1

            arrival_times.append(current_time)

            # Time until next arrival
            next_arrival = random.randint(1, 10)
            events.append([ARRIVAL, current_time + next_arrival])

            if queue_count == 1:  # Queue was empty
                # Time until next departure
                next_departure = random.randint(0, 10)
                events.append([DEPARTURE, current_time + next_departure])
        elif current_state[EVENT_TYPE] == DEPARTURE:
            current_time = current_state[EVENT_TIME]
            queue_count -= 1
            departures_count += 1

            departure_times.append(current_time)

            if queue_count > 0:  # Queue is not empty
                # Time until next departure
                next_departure = random.randint(0, 10)
                events.append([DEPARTURE, current_time + next_departure])


toll()
