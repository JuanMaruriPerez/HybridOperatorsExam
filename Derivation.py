from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
import binascii
import os

INPUT_DIR = "KEYS_COMBINED"
OUTPUT_DIR = "KEYS_DERIVED"

FILES = {
    "concatenation.txt": "concatenationDerived.txt",
    "hash.txt": "hashDerived.txt",
    "hmac.txt": "hmacDerived.txt",
    "xwing.txt": "xwingDerived.txt"
}

def derive_key(shared_key_hex):
    """Aplica HKDF-SHA256 para derivar una clave de 16 bytes."""
    shared_key = binascii.unhexlify(shared_key_hex.strip())

    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"",
    )
    return hkdf.derive(shared_key)

def process_file(input_filename, output_filename):
    input_path = os.path.join(INPUT_DIR, input_filename)
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    with open(input_path, "r") as f_in, open(output_path, "w") as f_out:
        for line in f_in:
            try:
                derived = derive_key(line)
                f_out.write(derived.hex() + "\n")
            except Exception as e:
                print(f"Error derivando clave de {input_filename}: {e}")

def main():
    for input_file, output_file in FILES.items():
        process_file(input_file, output_file)
    print("✅ Claves derivadas generadas correctamente.")

if __name__ == "__main__":
    main()
