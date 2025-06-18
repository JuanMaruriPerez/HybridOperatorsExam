import math
from collections import Counter
import numpy as np
import os
import sys
import matplotlib.pyplot as plt  # <-- Se añade para graficar

# Crear carpetas si no existen
os.makedirs("RESULTS", exist_ok=True)
os.makedirs("PLOT", exist_ok=True)

# Redirigir toda la salida estándar a un archivo
sys.stdout = open("RESULTS/result.txt", "w")

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

def calculate_average_entropy_from_file(filepath):
    entropies = []
    with open(filepath, "r") as f:
        for line in f:
            hex_string = line.strip()
            if hex_string:
                byte_data = bytes.fromhex(hex_string)
                entropy = shannon_entropy(byte_data)
                entropies.append(entropy)
    average_entropy = sum(entropies) / len(entropies) if entropies else 0.0
    return average_entropy

def calculate_global_entropy_from_counts(counts):
    total = sum(counts)
    if total == 0:
        return 0.0
    entropy = 0.0
    for count in counts:
        if count > 0:
            p = count / total
            entropy -= p * math.log2(p)
    return entropy


def byte_distribution_from_file(filepath):
    total_bytes = []
    with open(filepath, "r") as f:
        for line in f:
            hex_string = line.strip()
            if hex_string:
                byte_data = bytes.fromhex(hex_string)
                total_bytes.extend(byte_data)
    counter = Counter(total_bytes)
    full_counts = [counter.get(i, 0) for i in range(256)]
    return full_counts

def print_block_avg_frequencies(full_counts, block_size=8):
    n_blocks = 256 // block_size
    for i in range(n_blocks):
        block_sum = sum(full_counts[i*block_size:(i+1)*block_size])
        block_avg = block_sum / block_size
        diff = -(np.array(counts).mean()- block_avg)
        print(f"  Bloque {i+1:02d}: frecuencia media = {block_avg:.2f} : {diff:.2f}")


def print_distribution_stats(counts):
    arr = np.array(counts)
    total = arr.sum()

    print(f"  Total de bytes     : {total}")

    # Media teórica de frecuencias (si fuera perfectamente uniforme)
    theoretical_mean = total / 256
    print(f"  Media              : {theoretical_mean:.2f}")
    print(f"  Desviación estándar: {arr.std():.2f}")
    print(f"  Mínimo             : {arr.min()}")
    print(f"  Máximo             : {arr.max()}")
    print(f"  Byte más frecuente : {np.argmax(arr)} con {arr.max()} apariciones\n")

    print_block_avg_frequencies(counts, block_size=8)

def plot_distribution(counts, title, filename):
    """Genera un histograma de frecuencias de bytes con línea de referencia de la media teórica."""
    total = sum(counts)
    theoretical_mean = total / 256  # Valor esperado si la distribución es uniforme

    plt.figure(figsize=(12, 5))
    bars = plt.bar(range(256), counts, color='steelblue', label="Frecuencia observada")
    
    # Línea de la media teórica
    plt.axhline(y=theoretical_mean, color='red', linestyle='--', linewidth=2, label=f"Media teórica = {theoretical_mean:.2f}")
    
    plt.title(f"Distribución de Frecuencias - {title}")
    plt.xlabel("Valor del byte (0-255)")
    plt.ylabel("Frecuencia")
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join("PLOT", filename))
    plt.close()

# Ejecución principal
if __name__ == "__main__":
    filepaths = [
        "KEYS/ECDH.txt",
        "KEYS/KEM.txt",
        "KEYS_COMBINED/concatenation.txt",
        "KEYS_COMBINED/hash.txt",
        "KEYS_COMBINED/hmac.txt",
        "KEYS_COMBINED/xwing.txt",
        "KEYS_DERIVED/concatenationDerived.txt",
        "KEYS_DERIVED/hashDerived.txt",
        "KEYS_DERIVED/hmacDerived.txt",
        "KEYS_DERIVED/xwingDerived.txt"
    ]

    for path in filepaths:
        name = path.replace("/", "_").replace(".txt", "")
        print(f"\n📁 Analizando: {path}")

        counts = byte_distribution_from_file(path)

        global_entropy = calculate_global_entropy_from_counts(counts)
        print(f"🌐 Entropía global del conjunto de claves: {global_entropy:.4f} bits por byte")
        avg_entropy = calculate_average_entropy_from_file(path)
        print(f"🔐 Entropía media por clave: {avg_entropy:.4f} bits por byte")

        
        print_distribution_stats(counts)
        
        # 🖼️ Guardar gráfico
        plot_distribution(counts, title=name, filename=f"{name}.png")

        