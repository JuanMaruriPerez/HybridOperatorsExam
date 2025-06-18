from cryptography.hazmat.primitives.asymmetric import x448
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.kdf.hkdf import HKDF

def generate_ecdh_key():
    """Genera una clave simétrica usando ECDH con X448."""
    # Generación de claves privadas para ambas partes
    private_key_a = x448.X448PrivateKey.generate()
    private_key_b = x448.X448PrivateKey.generate()

    # Intercambio de claves públicas
    public_key_a = private_key_a.public_key()
    public_key_b = private_key_b.public_key()

    # Acuerdo de clave
    shared_key_a = private_key_a.exchange(public_key_b)
    shared_key_b = private_key_b.exchange(public_key_a)

    # Compruebo claves generadas son las mismas
    assert shared_key_a == shared_key_b, "Error: las claves compartidas no coinciden"

    # Derivación de clave simétrica (ejemplo comentado)
    # derived_key = HKDF(
    #     algorithm=hashes.SHA256(),
    #     length=32,
    #     salt=None,
    #     info=b'key agreement'
    # ).derive(shared_key_a)

    return shared_key_a, public_key_a, public_key_b

# Genera una clave de ejemplo
def prueba_generate_key():
    key, puba, pubb = generate_ecdh_key()
    print(f"Clave ECDH (X448): {key.hex()}")  # 56 bytes

if __name__ == "__main__":
    prueba_generate_key()
