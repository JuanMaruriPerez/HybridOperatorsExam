import numpy as np
import os

from ClassicKeyGenerator import generate_ecdh_key
from PQCKeyGenerator import generate_mlkem768_key

from cryptography.hazmat.primitives import serialization

def generate_keys(method, num_keys=500000):
    """Genera un conjunto de claves usando el método especificado."""
    keys = []
    for _ in range(num_keys):
        keys.append(method())
    return keys

def KeysGenerator():
    # Generación de claves
    ecdh_triples = generate_keys(generate_ecdh_key, num_keys=500000)
    mlkem_keys = generate_keys(generate_mlkem768_key, num_keys=500000)

    # Extrae shared_key, public_key_a y public_key_b
    shared_keys_bytes = [np.frombuffer(shared_key, dtype=np.uint8) for shared_key, _, _ in ecdh_triples]
    #puba_bytes = [np.frombuffer(puba.public_bytes_raw(), dtype=np.uint8) for _, puba, _ in ecdh_triples]
    #pubb_bytes = [np.frombuffer(pubb.public_bytes_raw(), dtype=np.uint8) for _, _, pubb in ecdh_triples]
    puba_bytes = [np.frombuffer(puba.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    ), dtype=np.uint8) for _, puba, _ in ecdh_triples]
    pubb_bytes = [np.frombuffer(pubb.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    ), dtype=np.uint8) for _, _, pubb in ecdh_triples]

    # ML-KEM
    mlkem_keys_bytes = [np.frombuffer(key, dtype=np.uint8) for key in mlkem_keys]

    return shared_keys_bytes, mlkem_keys_bytes, puba_bytes, pubb_bytes

def save_keys_to_files(shared_keys, mlkem_keys, puba_keys, pubb_keys, folder="KEYS"):
    os.makedirs(folder, exist_ok=True)

    def save_list_to_file(data_list, filename):
        path = os.path.join(folder, filename)
        with open(path, "w") as f:
            for item in data_list:
                f.write(item.tobytes().hex() + "\n")

    save_list_to_file(shared_keys, "ECDH.txt")
    save_list_to_file(mlkem_keys, "KEM.txt")
    save_list_to_file(puba_keys, "puba.txt")
    save_list_to_file(pubb_keys, "pubb.txt")

# Genera y guarda claves
def prueba_generate_key():
    shared_keys, mlkem_keys, puba_keys, pubb_keys = KeysGenerator()
    save_keys_to_files(shared_keys, mlkem_keys, puba_keys, pubb_keys)

if __name__ == "__main__":
    prueba_generate_key()