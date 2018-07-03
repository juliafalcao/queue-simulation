from experiment import *

utilizations_16 = []
drop_rates_16 = []
avg_requisition_times_16 = []
avg_queue_sizes_16 = []

for i in range(16):
    seed_x = random.randint(0, 9999999999999999999999)
    seed_c = random.randint(0, 9999999999999999999999)
    utilizations, drop_rates, avg_requisition_times, avg_queue_sizes = experiment(seed_x, seed_c)
    utilizations_16.append(utilizations)
    drop_rates_16.append(drop_rates)
    avg_requisition_times_16.append(avg_requisition_times)
    avg_queue_sizes_16.append(avg_queue_sizes)

# measures
avg_utilizations = ["_" for i in range(6)]
avg_drop_rates = ["_" for i in range(6)]

for i in range(6): # six variations of E[C]
    avg_utilizations[i] = sum(utilizations_16[i]) / float(16)
    avg_drop_rates[i] = sum(drop_rates_16[i]) / float(16)

print(avg_utilizations)
print(avg_drop_rates)

Ec_variations = [0.10, 0.12, 0.14, 0.16, 0.18, 0.20]
x_values = [1/Ec for Ec in Ec_variations]
plt.title("Média da Utilização (16 experimentos)")
plt.plot(x_values, avg_utilizations, linewidth = 2, color = "darkviolet")
plt.xlabel("Taxas de chegada (1/E[C])")
plt.ylabel("Utilização média")
plt.savefig("media_utilizacoes.png")
plt.clf()

plt.title("Média da Taxa de Descarte (16 experimentos)")
plt.plot(x_values, avg_drop_rates, linewidth = 2, color = "darkviolet")
plt.xlabel("Taxas de chegada (1/E[C])")
plt.ylabel("Taxa de descarte média")
plt.savefig("media_taxa_descarte.png")