from generators import *
from simulator import *
import matplotlib.pyplot as plt

Ec_variations = [0.200, 0.180, 0.160, 0.140, 0.120, 0.110, 0.100] # seconds
Ex = 0.09 # seconds

utilizations = []
drop_rates = []
avg_requisition_times = []
avg_queue_sizes = []

for Ec in Ec_variations:
    measures = restaurant_simulator(simulation_time = 3600, arrival_rate = float(1/Ec), service_rate = float(1/Ex))
    utilizations.append(measures["utilization"])
    drop_rates.append(measures["drop_rate"])
    avg_queue_sizes.append(measures["avg_queue_size"])
    avg_requisition_times.append(measures["avg_requisition_time"])

print(drop_rates)

x_values = [1/Ec for Ec in Ec_variations]
xticks = ["1/" + str(Ec) for Ec in Ec_variations]
plt.plot(Ec_variations, drop_rates, linewidth = 2, color = "darkviolet")
plt.show()