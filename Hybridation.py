from cryptography.hazmat.primitives import hashes, hmac
import os

def read_keys(file_path):
    """Lee las claves de un fichero y devuelve una lista de bytes."""
    with open(file_path, "r") as f:
        keys = [bytes.fromhex(line.strip()) for line in f.readlines()]
    return keys

def write_lines(file_path, lines):
    """Escribe una lista de líneas en un fichero."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        for line in lines:
            f.write(line + "\n")

def concatenate_keys(ecdh_keys, kem_keys):
    """Concatena las claves ecdh y kem fila a fila."""
    if len(ecdh_keys) != len(kem_keys):
        raise ValueError("Los ficheros tienen diferente número de claves")
    return [e + k for e, k in zip(ecdh_keys, kem_keys)]

def hash_keys(concatenated_keys, hash_algorithm=hashes.SHA256()):
    """Aplica hash a las claves concatenadas usando cryptography."""
    hashes_list = []
    for key in concatenated_keys:
        digest = hashes.Hash(hash_algorithm)
        digest.update(key)
        hashes_list.append(digest.finalize().hex())
    return hashes_list

def hmac_keys(concatenated_keys, hmac_key=b"secret_hmac_key", hash_algorithm=hashes.SHA256()):
    """Aplica HMAC a las claves concatenadas usando cryptography."""
    hmacs = []
    for key in concatenated_keys:
        h = hmac.HMAC(hmac_key, hash_algorithm)
        h.update(key)
        hmacs.append(h.finalize().hex())
    return hmacs

def hybridation(hash_algorithm=hashes.SHA256(), hmac_key=b""):
    # Leer claves básicas
    ecdh_keys = read_keys("KEYS/ECDH.txt")
    kem_keys = read_keys("KEYS/KEM.txt")

    # Concatenación ECDH + KEM
    concatenated = concatenate_keys(ecdh_keys, kem_keys)
    write_lines("KEYS_COMBINED/concatenation.txt", [c.hex() for c in concatenated])

    # Hash tradicional
    hashed = hash_keys(concatenated, hash_algorithm)
    write_lines("KEYS_COMBINED/hash.txt", hashed)

    # HMAC
    hmaced = hmac_keys(concatenated, hmac_key, hash_algorithm)
    write_lines("KEYS_COMBINED/hmac.txt", hmaced)

    # --- X-Wing: leer claves públicas ---
    puba_keys = read_keys("KEYS/puba.txt")
    pubb_keys = read_keys("KEYS/pubb.txt")

    if not (len(ecdh_keys) == len(kem_keys) == len(puba_keys) == len(pubb_keys)):
        raise ValueError("Los ficheros no tienen el mismo número de entradas")

    # Concatenar ECDH + KEM + pubA + pubB
    xwing_inputs = [
        e + k + puba + pubb
        for e, k, puba, pubb in zip(ecdh_keys, kem_keys, puba_keys, pubb_keys)
    ]

    # Hash de X-Wing
    xwing_hashes = hash_keys(xwing_inputs, hash_algorithm)
    write_lines("KEYS_COMBINED/xwing.txt", xwing_hashes)

if __name__ == "__main__":
    from cryptography.hazmat.primitives import hashes
    hybridation(hash_algorithm=hashes.SHA256(), hmac_key=b"")
