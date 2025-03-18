# CppCrypt

---

## Description

This is a learning project about the Diffie-Hellman (DH) key-exchange and Advanced Encryption Standard (AES).

Goal of the project is to implement following **Features**
- Encrypt and save text files in an encrypted state, as well as vice versa
- Send text files via TCP using DH for key exchange followed up by AES for encryption

### Directory Structure

---

```plaintext
├── aesify.py
├── cryptology
│   ├── aes
│   │   ├── aes.cpp
│   │   ├── aes.h
│   │   ├── __init__.py
│   │   ├── module.cpp
│   │   └── setup.py
│   ├── __init__.py
│   ├── prim_roots
│   │   ├── __init__.py
│   │   ├── prim_roots.cpp
│   │   └── setup.py
│   └── utils.py
├── diffify.py
├── LICENSE.txt
├── main.py
├── README.md
└── requirements.txt
```

### Content description

---

The subdirectory `prim_roots` contains a module named `primitive_roots` for verification of prime numbers and calculation of their primitive roots and is used for DH.

The subdirectory `aes` contains a module named `pyaes` which contains function definitions for key-expansion from key to round keys, as well as encryption and decryption of sixteen bytes, formatted as 4x4 matrix.

The `aesify.py` script encrypts and decrypts textfiles.

The `diffify.py` script exchanges keys per DH and sends a via AES encrypted file from host to client afterwards.

## Installation

--- 

To install the necessary packages from the Python package index run

```bash
pip install -r requirements.txt
```

To install the C++ components change directory into `aes` and `prim_roots` respectively and run

```bash
python setup.py build_ext --inplace
```

## Usage of AES

---

Given a textfile called `lore.txt` containing plaintext

### Encryption

```bash
python aesify.py -en lore.txt crypted_lore.txt 
```

### Decryption

#### Print

To just print the contents of a previously encrypted file into the terminal run

```bash
python aesify.py -de crypted_lore.txt -p
```

#### Save to txt

To save the contents of a previously encrypted file as plaintext run

```bash
python aesify.py -de crypted_lore.txt decrypted_lore.txt
```

## Usage of diffie.py

---

**⚠ Warning**: The current implementation uses 64-bit prime numbers, which are insecure for real-world use.

### Run as host:

```bash
python diffify.py h
```

### Run as client:

```bash
python diffify.py c
```

## License 

---

This project is licensed under the MIT license.
