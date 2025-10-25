import os
import sys
import argparse
from getpass import getpass
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, hashes

Max_File_Size = 1 * 1024 * 1024 #Membatasi ukuran file maksimal 1MB
Salt_Size = 16
IV_Size = 16
Key_Size = 32
PBKDF2_Iterations = 100000

def derive_key(password: str, salt: bytes) -> bytes:
    """
    password = password dari pengguna
    salt = random bytes agar menghasilkan kunci yang berbeda meskipun password sama,
    yang kemudian akan digunakan dalam PBKDF2 a.k.a kdf/key derivation function
    
    return =  kunci 256 bit, karena menggunakan AES-256
    """
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=Key_Size,
        salt=salt,
        iterations=PBKDF2_Iterations,
        backend=default_backend()
    )
    key = kdf.derive(password.encode('utf-8'))
    return key


def encrypt_file(input_path: str, output_path: str, password: str) -> bool:
    """
    Encrypt file menggunakan AES-256 CBC mode
    
    input_path = path ke file yang akan dienkripsi
    output_path = path untuk menyimpan file terenkripsi
    password = password untuk enkripsi
    
    return = True jika berhasil, False jika gagal
    """
    
    try:
        #Validasi input file
        if not os.path.exists(input_path):
            print(f"Error: file '{input_path}' tidak ditemukan.")
            return False
        
        #Validasi ukuran file
        file_size = os.path.getsize(input_path)
        if file_size > Max_File_Size:
            print(f"Error: ukuran file melebihi batas maksimal {Max_File_Size} bytes.")
            return False
        
        #Baca file input
        with open(input_path, 'rb') as f:
            plaintext = f.read()
            
            
        #Generate salt dan iv
        salt = os.urandom(Salt_Size)
        iv = os.urandom(IV_Size)
        
        #Generate kunci menggunakan fungsi derive_key
        key = derive_key(password, salt)
        
        #Padding
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext) + padder.finalize()

        #Enkripsi
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        #Simpan salt, iv, dan ciphertext ke file output
        with open(output_path, 'wb') as f:
            f.write(salt)
            f.write(iv)
            f.write(ciphertext)
            
        print(f"File berhasil dienkripsi dan disimpan di '{output_path}'.")
        print(f"  - Ukuran asli: {file_size} bytes")
        print(f"  - Ukuran terenkripsi: {os.path.getsize(output_path)} bytes")
        return True
    
    except Exception as e:
        print(f"Error saat enkripsi: {str(e)}")
        return False
    
    
def decrypt_file(input_path: str, output_path: str, password: str) -> bool:
    """
    Decrypt file yang telah di encrypt
    input_path = path ke file hasil encrypt
    output_path = path untuk menyimpan file hasil decrypt
    password = password untuk decrypt
        
    return = True jika berhasil, False jika gagal
    """
        
    try:
        #Validasi input file
        if not os.path.exists(input_path):
            print(f"Error: file '{input_path}' tidak ditemukan.")
            return False
            
        #Baca file input
        with open(input_path, 'rb') as f:
            encrypted_data = f.read()
           
        #Validasi ukuran file
        min_size = Salt_Size + IV_Size
        if len(encrypted_data) < min_size:
            print("Error: file terenkripsi terlalu kecil atau corrupt.")
            return False
        
        #Extract salt, iv, dan ciphertext
        salt = encrypted_data[:Salt_Size]
        iv = encrypted_data[Salt_Size:Salt_Size + IV_Size]
        ciphertext = encrypted_data[Salt_Size + IV_Size:]
        
        key = derive_key(password, salt)
        
        #Decrypt
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        #Delete padding
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        
        #Simpan hasil decrypt ke file output
        with open(output_path, 'wb') as f:
            f.write(plaintext)
            
        print(f"File berhasil didekripsi dan disimpan di '{output_path}'.")
        print(f"  - Ukuran file: {len(plaintext)} bytes")
        return True
    
    except ValueError as e:
        print("Error: Password salah atau file corrupt.")
        return False
    
    except Exception as e:
        print(f"Error saat dekripsi: {str(e)}")
        return False
    
def main():
    parser = argparse.ArgumentParser(
        description="Alat Enkripsi dan Dekripsi File menggunakan AES-256 CBC",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Contoh penggunaan:
  Enkripsi file:
    python crypto_cli.py encrypt data.csv data.csv.enc
  
  Dekripsi file:
    python crypto_cli.py decrypt data.csv.enc data_decrypted.csv
    """
    )
    
    parser.add_argument(
        'mode',
        choices=['encrypt', 'decrypt'],
        help="Mode operasi: encrypt atau decrypt"
    )
    parser.add_argument(
        'input_file',
        help="Path ke file input"
    )
    parser.add_argument(
        'output_file',
        help="Path ke file output"
    )
    parser.add_argument(
        '-p', '--password',
        help="Password untuk enkripsi/dekripsi (jika tidak diberikan, akan diminta secara interaktif)"
    )
    
    args = parser.parse_args()
    
    if args.password:
        password = args.password
    else:
        password = getpass("Masukkan password untuk {args.mode}: ")
        if not password:
            print("Error: password tidak boleh kosong.")
            sys.exit(1)
            
    print(f"\n{'='*50}")
    print(f"Mode: {args.mode.upper()}")
    print(f"File input: {args.input_file}")
    print(f"File output: {args.output_file}")
    print(f"{'='*50}\n")
    
    if args.mode == 'encrypt':
        success = encrypt_file(args.input_file, args.output_file, password)
    else:
        success = decrypt_file(args.input_file, args.output_file, password)
    
    if success:
        print("\n✓ Operasi selesai dengan sukses!")
        sys.exit(0)
    else:
        print("\n✗ Operasi gagal!")
        sys.exit(1)


if __name__ == '__main__':
    main()