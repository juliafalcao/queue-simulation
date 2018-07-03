from generators import *
from simulator import *
import matplotlib.pyplot as plt

Ec_variations = [0.10, 0.12, 0.14, 0.16, 0.18, 0.20] # seconds
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

x_values = [1/Ec for Ec in Ec_variations]
plt.plot(x_values, drop_rates, linewidth = 2, color = "darkviolet")
# plt.xticks(x_values, ["1/" + str(Ec) for Ec in Ec_variations])
plt.xlabel("Taxas de chegada (1/E[C])")
plt.ylabel("Taxa de descarte")
plt.title("Taxas de descarte")
plt.savefig("taxas_descarte.png")
plt.clf()

plt.plot(x_values, utilizations, linewidth = 2, color = "darkviolet")
plt.xlabel("Taxas de chegada (1/E[C])")
plt.ylabel("Utilização")
plt.title("Utilizações")
plt.savefig("utilizacao.png")
plt.clf()

plt.plot(x_values, avg_requisition_times, linewidth = 2, color = "darkviolet")
plt.xlabel("Taxas de chegada (1/E[C])")
plt.ylabel("Tempo médio")
plt.title("Tempo médio que as requisições permanecem no sistema")
plt.savefig("tempo_medio_espera.png")
plt.clf()