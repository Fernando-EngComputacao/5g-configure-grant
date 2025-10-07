import numpy as np
import matplotlib.pyplot as plt

# Carrega os atrasos do Sym e do RB (em ns)
sym = np.loadtxt("delays_sym.txt")
rb = np.loadtxt("delays_rb.txt")

# Converte para milissegundos
sym_ms = sym / 1e6
rb_ms = rb / 1e6

# Cálculos
print(f"Sym-OFDMA: Média = {np.mean(sym_ms):.3f} ms | Desvio = {np.std(sym_ms):.3f} ms")
print(f"RB-OFDMA:  Média = {np.mean(rb_ms):.3f} ms | Desvio = {np.std(rb_ms):.3f} ms")

# Gráfico comparativo
plt.figure()
plt.boxplot([sym_ms, rb_ms], labels=["Sym-OFDMA", "RB-OFDMA"])
plt.ylabel("Delay (ms)")
plt.title("Comparação de Atraso PDCP entre Sym-OFDMA e RB-OFDMA")
plt.grid(True)
plt.show()
