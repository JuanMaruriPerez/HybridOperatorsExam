import oqs

def generate_mlkem768_key():
    """Genera una clave simétrica usando Kyber768."""
    with oqs.KeyEncapsulation("Kyber768") as kem:
        # Genera clave pública y privada
        public_key = kem.generate_keypair()

        # Encapsula para derivar la clave simétrica
        ciphertext, _ = kem.encap_secret(public_key)
        shared_secret = kem.decap_secret(ciphertext)

        #Prueba concatenacion robusta
        return shared_secret


# Genera una clave de ejemplo
def prueba_generate_key():
    key = generate_mlkem768_key()
    print(f"Clave KEM (mlkem768): {key.hex()}") # 32 b


if __name__ == "__main__":
    prueba_generate_key()