# Test.py

import os
import math
import numpy as np
from scipy.stats import chisquare
from scipy.spatial.distance import jensenshannon
from collections import Counter

# Archivos a analizar
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

def byte_distribution(filepath):
    """Devuelve un array con la cuenta de cada byte (0-255)."""
    total_bytes = []
    with open(filepath, "r") as f:
        for line in f:
            hex_string = line.strip()
            if hex_string:
                total_bytes.extend(bytes.fromhex(hex_string))
    counter = Counter(total_bytes)
    return np.array([counter.get(i, 0) for i in range(256)])

def run_statistical_tests(counts):
    total = counts.sum()
    expected = np.full(256, total / 256)

    # Test Chi-cuadrado
    chi2_stat, chi2_pval = chisquare(counts, expected)

    # Jensen-Shannon distance (usamos probabilidades normalizadas)
    empirical = counts / total
    uniform = np.full(256, 1/256)
    js_distance = jensenshannon(empirical, uniform, base=2)

    return chi2_stat, chi2_pval, js_distance

def main():
    print("🔍 Resultados de Pruebas Estadísticas sobre Distribución de Bytes:\n")
    print(f"{'Fichero':<45} {'Chi²':>10} {'p-valor':>10} {'JSD':>10}")
    print("-" * 75)

    for path in filepaths:
        counts = byte_distribution(path)
        chi2_stat, chi2_pval, js_dist = run_statistical_tests(counts)

        name = path.replace("KEYS/", "").replace("KEYS_COMBINED/", "").replace("KEYS_DERIVED/", "").replace(".txt", "")
        print(f"{name:<45} {chi2_stat:10.2f} {chi2_pval:10.4f} {js_dist:10.4f}")

if __name__ == "__main__":
    main()
