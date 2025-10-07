import numpy as np
import matplotlib.pyplot as plt

# Carrega os atrasos do Sym e do RB (em ns)
sym = np.loadtxt("delays_sym_20MHz.txt")
rb = np.loadtxt("delays_rb_20MHz.txt")
otdma = np.loadtxt("delays_5gl_tdma_20MHz.txt")
gl_ofdma = np.loadtxt("delays_5gl_ofdma_20MHz.txt")

# Converte para milissegundos
sym_ms = sym / 1e6
rb_ms = rb / 1e6
otdma_ms = otdma / 1e6
gl_ofdma_ms = gl_ofdma / 1e6

# Cálculos
print(f"RB-OFDMA:  Média = {np.mean(rb_ms):.3f} ms | Desvio = {np.std(rb_ms):.3f} ms")
print(f"5GL-OFDMA: Média = {np.mean(gl_ofdma_ms):.3f} ms | Desvio = {np.std(gl_ofdma_ms):.3f} ms")
print(f"Sym-OFDMA: Média = {np.mean(sym_ms):.3f} ms | Desvio = {np.std(sym_ms):.3f} ms")
print(f"5GL-TDMA:  Média = {np.mean(otdma_ms):.3f} ms | Desvio = {np.std(otdma_ms):.3f} ms")

# Gráfico comparativo
plt.figure()
plt.boxplot([rb_ms, gl_ofdma_ms, sym_ms, otdma_ms], labels=["RB-OFDMA", "5GL-OFDMA", "Sym-OFDMA", "5GL-TDMA"])
plt.ylabel("Latency (ms)")
plt.title("20 MHz") #Packet PDCP Delay
plt.grid(True)
plt.show()
