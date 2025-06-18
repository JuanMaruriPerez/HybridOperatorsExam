import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Lista de archivos a analizar
FILEPATHS = [
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

def read_byte_sequences(filepath):
    with open(filepath, "r") as f:
        return [bytes.fromhex(line.strip()) for line in f if line.strip()]

def compute_correlation_matrix(sequences):
    M = np.zeros((256, 256), dtype=int)
    for seq in sequences:
        for i in range(len(seq)-1):
            M[seq[i], seq[i+1]] += 1
    return M

def save_csv(matrix, name):
    # DataFrame con filas y columnas etiquetadas b00..bFF
    labels = [f"b{v:02X}" for v in range(256)]
    df = pd.DataFrame(matrix, index=labels, columns=labels)
    os.makedirs("CORRELATION", exist_ok=True)
    path = f"CORRELATION/{name}_correlation.csv"
    df.to_csv(path)
    print(f"[+] Guardado CSV: {path}")

#def plot_3d(matrix, name):
#    X, Y = np.meshgrid(np.arange(256), np.arange(256))
#    Z = matrix
#
#    fig = plt.figure(figsize=(10,8))
#    ax = fig.add_subplot(111, projection='3d')
#    ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
#    ax.set_xlabel('Byte siguiente (j)')
#    ax.set_ylabel('Byte actual (i)')
#    ax.set_zlabel('Frecuencia')
#    ax.set_title(f"Correlación Byte→Byte: {name}")

#    os.makedirs("CORRELATION", exist_ok=True)
#    out = f"CORRELATION/{name}_correlation3d.png"
#    plt.tight_layout()
#    plt.savefig(out)
#    plt.close()
#    print(f"[+] Guardado gráfico 3D: {out}")

def plot_all_views(matrix, name):
    """Dibuja y guarda 4 vistas diferentes de la misma superficie 3D."""
    X, Y = np.meshgrid(np.arange(256), np.arange(256))
    Z = matrix
    os.makedirs("CORRELATION", exist_ok=True)

    def _save_view(elev, azim, suffix):
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        #ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
        surf = ax.plot_surface(
            X, Y, Z, cmap='viridis', edgecolor='none', 
            rcount=100, ccount=100, antialiased=True
        )
        ax.set_xlabel('Byte siguiente (j)')
        ax.set_ylabel('Byte actual (i)')
        ax.set_zlabel('Frecuencia')
        ax.set_title(f"{name} - {suffix} view")
        ax.view_init(elev=elev, azim=azim)
        
        # Añadimos la colorbar como leyenda
        cbar = fig.colorbar(surf, ax=ax, shrink=0.6, aspect=10, pad=0.1)
        cbar.set_label('Frecuencia absoluta')
        
        out = f"CORRELATION/{name}_correlation3d_{suffix}.png"
        plt.tight_layout()
        plt.savefig(out)
        plt.close()
        print(f"[+] Guardada vista {suffix}: {out}")

    # Vista por defecto
    _save_view(elev=30, azim=-60, suffix="default")
    # Vista XY (cenital): elev=90 (mirando desde arriba), azim any (0)
    _save_view(elev=90, azim=0, suffix="XY")
    # Vista XZ (frontal): elev=0 (mirando frente), azim=0
    _save_view(elev=0, azim=0, suffix="XZ")
    # Vista YZ (lateral): elev=0, azim=90 (mirando en la otra horizontal)
    _save_view(elev=0, azim=90, suffix="YZ")


if __name__ == "__main__":
    for filepath in FILEPATHS:
        name = os.path.splitext(os.path.basename(filepath))[0]
        print(f"\nProcesando: {filepath}")
        seqs = read_byte_sequences(filepath)
        matrix = compute_correlation_matrix(seqs)
        save_csv(matrix, name)
        #plot_3d(matrix, name)
        plot_all_views(matrix, name)
