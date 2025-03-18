# Python module for Cryptography written in C++

---

## Directory Structure

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
