# Aplikasi Kriptografi CLI - AES-256 CBC Sederhana

Aplikasi dengan basis CLI untuk enkripsi dan dekripsi file menggunakan algoritma AES-256 (CBC mode) dengan manajemen kunci berbasis password.

## 📋 Deskripsi

Aplikasi ini dibuat untuk memenuhi tugas mata kuliah Keamanan Data Program Studi Sarjana Data Science, Universitas Telkom Bandung. Aplikasi ini mengimplementasikan enkripsi simetris menggunakan AES-256 dalam mode CBC (Cipher Block Chaining) dengan key derivation function PBKDF2.

## 🔐 Fitur Utama

- ✅ **Enkripsi File**: Mengenkripsi file dengan AES-256 CBC mode
- ✅ **Dekripsi File**: Mendekripsi file yang telah dienkripsi
- ✅ **Manajemen Kunci Berbasis Password**: Menggunakan PBKDF2 untuk menurunkan kunci dari password
- ✅ **Keamanan Tinggi**: Salt dan IV unik untuk setiap enkripsi
- ✅ **Penanganan Error**: Pesan error yang jelas untuk berbagai kondisi
- ✅ **Batasan Ukuran**: Mendukung file hingga 1 MB

## 📦 Persyaratan Sistem

- Python 3.7 atau lebih baru
- Library `cryptography`

## 🚀 Instalasi

1. Pastikan Python 3 sudah terinstal di sistem Anda:
```bash
python --version
```

2. Install library yang diperlukan:
```bash
pip install cryptography
```

## 💻 Cara Penggunaan

### Format Umum (pastikan file data berada di path yang sama dengan file aplikasi)
```bash
python crypto_cli.py [mode (encrypt atau decrypt)] [input_file] [output_file] [-p PASSWORD]
```

### Enkripsi File

**Metode 1: Password interaktif (Direkomendasikan)**
```bash
python crypto_cli.py encrypt data.csv data.csv.enc
```
Program akan meminta Anda memasukkan password secara aman.

**Metode 2: Password sebagai argumen**
```bash
python crypto_cli.py encrypt data.csv data.csv.enc -p MySecretPassword123
```

### Dekripsi File

**Metode 1: Password interaktif (Direkomendasikan)**
```bash
python crypto_cli.py decrypt data.csv.enc data_decrypted.csv
```

**Metode 2: Password sebagai argumen**
```bash
python crypto_cli.py decrypt data.csv.enc data_decrypted.csv -p MySecretPassword123
```

## 📝 Contoh Penggunaan

### Contoh 1: Enkripsi file CSV
```bash
# Enkripsi file dataset.csv
python crypto_cli.py encrypt dataset.csv dataset.csv.enc

# Output:
# ==================================================
# Mode: ENCRYPT
# File input: dataset.csv
# File output: dataset.csv.enc
# ==================================================
# 
# Masukkan password untuk encrypt: ********
# ✓ File berhasil dienkripsi: dataset.csv.enc
#   - Ukuran asli: 2048 bytes
#   - Ukuran terenkripsi: 2080 bytes
# 
# ✓ Operasi selesai dengan sukses!
```

### Contoh 2: Dekripsi file
```bash
# Dekripsi file yang telah dienkripsi
python crypto_cli.py decrypt dataset.csv.enc dataset_restored.csv

# Output:
# ==================================================
# Mode: DECRYPT
# File input: dataset.csv.enc
# File output: dataset_restored.csv
# ==================================================
# 
# Masukkan password untuk decrypt: ********
# ✓ File berhasil didekripsi: dataset_restored.csv
#   - Ukuran file: 2048 bytes
# 
# ✓ Operasi selesai dengan sukses!
```

## 🔒 Detail Teknis Implementasi

### Algoritma Kriptografi
- **Algoritma**: AES (Advanced Encryption Standard)
- **Ukuran Kunci**: 256-bit
- **Mode**: CBC (Cipher Block Chaining)
- **Padding**: PKCS7

### Key Derivation Function (KDF)
- **Algoritma**: PBKDF2 (Password-Based Key Derivation Function 2)
- **Hash Function**: SHA-256
- **Iterasi**: 100,000 iterasi
- **Salt Size**: 16 bytes (unik untuk setiap enkripsi)

### Initialization Vector (IV)
- **Ukuran**: 16 bytes (128-bit, sesuai block size AES)
- **Generasi**: Random unik untuk setiap enkripsi

### Format File Terenkripsi
```
[Salt: 16 bytes] + [IV: 16 bytes] + [Ciphertext: variable]
```

## ⚠️ Batasan & Catatan Penting

1. **Ukuran File**: Aplikasi hanya mendukung file dengan ukuran maksimal 1 MB
2. **Password**: Gunakan password yang kuat dan mudah diingat
3. **Keamanan Password**: Disarankan menggunakan mode interaktif (tanpa flag -p) agar password tidak tercatat di command history
4. **Backup**: Selalu simpan backup file asli sebelum enkripsi

## ❌ Penanganan Error

### Error: File tidak ditemukan
```bash
Error: File 'data.csv' tidak ditemukan.
```
**Solusi**: Pastikan path file input benar

### Error: Password salah
```bash
Error: Password salah atau file rusak.
```
**Solusi**: Periksa kembali password yang digunakan

### Error: Ukuran file terlalu besar
```bash
Error: Ukuran file (2097152 bytes) melebihi batas maksimal (1 MB).
```
**Solusi**: Gunakan file dengan ukuran ≤ 1 MB

## 📚 Referensi

- [Cryptography Library Documentation](https://cryptography.io/)
- [AES (Advanced Encryption Standard)](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
- [PBKDF2](https://en.wikipedia.org/wiki/PBKDF2)
- [CBC Mode](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#CBC)

## 👨‍🎓 Informasi Pengembang

- **Dibuat untuk**: Tugas Mata Kuliah Keamanan Data
- **Program Studi**: Sarjana Data Science
- **Universitas**: Universitas Telkom Bandung

## 📄 Lisensi

Aplikasi ini dibuat untuk tujuan pendidikan sebagai bagian dari tugas kuliah.

---

**Catatan**: Aplikasi ini dirancang untuk tujuan pembelajaran. Untuk penggunaan produksi yang sesungguhnya, pertimbangkan untuk menggunakan solusi kriptografi yang sudah teruji dan diaudit secara profesional.
