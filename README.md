# CppCrypt

---

## Description

This is a learning project about the Diffie-Hellman (DH) key-exchange and Advanced Encryption Standard (AES).

Goal of the project is to implement following **Features**
- Encrypt and save text files in an encrypted state, as well as vice versa
- Send text files via TCP using DH for key exchange followed up by AES for encryption

### Content description

---

The subdirectory `prim_roots` contains a module named `primitive_roots` for verification of prime numbers and calculation of their primitive roots and is used for DH.

The subdirectory `aes` contains a module named `pyaes` which contains function definitions for key-expansion from key to round keys, as well as encryption and decryption of sixteen bytes, formatted as 4x4 matrix.

The `aesify.py` script encrypts and decrypts textfiles.

The `ecdiffify.py` script exchanges keys per DH and sends a via AES encrypted file from host to client afterwards.

### Development Environment

---

- **Operating System**: Fedora Linux 41 (Workstation Edition)
- **Python**: 3.12.3
- **g++ (GCC)**: 14.2.1 (Red Hat 14.2.1-7)

### Dependencies

---

```plaintext
build           1.2.2.post1
numpy           2.2.4
packaging       24.2
pip             25.0.1
pyaes           0.1.0
pybind11        2.13.6
pyproject_hooks 1.2.0
setuptools      78.0.1
```

## Installation

--- 
To install dependencies for building the C++ extensions (on Fedora) run

```bash 
sudo dnf install python3-devel, gmp-devel
```

To install the necessary packages from the Python package index run

```bash
pip install -r requirements.txt
```

To build the C++ extensions run

```bash
python -m build cryptology/aes/ -n -w
```

To install the extensions as Python packages run

```bash
pip install cryptology/aes/dist/*.whl
```

## Usage of aesify.py

---

Given a textfile called `lore.txt` containing plaintext

### Encryption

After running 

```bash
python aesify.py -en lore.txt crypted_lore.txt 
```

you will be prompted to enter a passkey, which is expected to be expected to be 16 hexadecimal numbers in the range between 0 and FF separated by commas, like for example 

```plaintext
0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f
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

## Usage of ecdiffify.py

---

### Run as host:

```bash
python ecdiffify.py h
```

### Run as client:

```bash
python ecdiffify.py c
```

## License 

---

This project is licensed under the MIT license.
