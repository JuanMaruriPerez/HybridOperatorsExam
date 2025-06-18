import secrets
import math
import matplotlib.pyplot as plt

def shannon_entropy(byte_data):
    if not byte_data:
        return 0.0
    byte_counts = [0] * 256
    for byte in byte_data:
        byte_counts[byte] += 1
    entropy = 0.0
    length = len(byte_data)
    for count in byte_counts:
        if count == 0:
            continue
        p = count / length
        entropy -= p * math.log2(p)
    return entropy

entropies_per_key = []
lengths = range(2, 513, 2)  # Desde 2 hasta 512 bytes (saltos de 2)

for length in lengths:
    samples = [secrets.token_bytes(length) for _ in range(256)]
    sample_entropies = [shannon_entropy(sample) for sample in samples]
    avg_entropy = sum(sample_entropies) / len(sample_entropies)
    entropies_per_key.append(avg_entropy)

# Obtener valores de entropía para 16 y 32 bytes
entropy_16 = entropies_per_key[15]  # Índice para length=16 (2, 4, ..., 16 es el 8º elemento, índice 7)
entropy_32 = entropies_per_key[31]  # Índice para length=32 (índice 15)

# Graficar
plt.figure(figsize=(10, 6))
plt.plot(lengths, entropies_per_key, label="Entropía por clave", color="blue")
plt.scatter([32], [entropy_16], color="red", s=100, label="16 bytes", zorder=5)
plt.scatter([64], [entropy_32], color="green", s=100, label="32 bytes", zorder=5)

# Anotar los puntos
plt.annotate(f"{entropy_16:.2f} bits", (32, entropy_16), textcoords="offset points", xytext=(0, 10), ha="center", color="red")
plt.annotate(f"{entropy_32:.2f} bits", (64, entropy_32), textcoords="offset points", xytext=(0, 10), ha="center", color="green")

plt.xlabel("Longitud de la clave (bytes)")
plt.ylabel("Entropía (bits)")
plt.title("Entropía total por clave (empírica)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Imprimir valores de entropía para 16 y 32 bytes
print(f"Entropía para clave de 32 bytes: {entropy_16:.2f} bits")
print(f"Entropía para clave de 64 bytes: {entropy_32:.2f} bits")