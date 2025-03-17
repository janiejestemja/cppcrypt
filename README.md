# Python module for Cryptography written in C++

---

## Description

---

This is a learning project about the Diffie-Hellman key-exchange (DH) as well as the advanced ecryption standard (AES) thus this software is meant for learning and experimentation, not real world application. 

**Features**
- Encrypt and save files in an encrypted state, as well as vice versa
- Send encrypted textfiles via TCP using DH followed up by AES

## Directory Structure

---

```plaintext
cppcrypt
├── aes
│   ├── aes.cpp
│   ├── aes.h
│   ├── __init__.py
│   ├── module.cpp
│   └── setup.py
├── diffie.py
├── main.py
├── prim_roots
│   ├── __init__.py
│   ├── prim_roots.cpp
│   └── setup.py
├── README.md
├── requirements.txt
└── utils.py
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
python main.py -en lore.txt crypted_lore.txt lore_key.txt
```

### Decryption

#### Print

To just print the contents of a previously encrypted file into the terminal run

```bash
python main.py -de crypted_lore.txt lore_key.txt -p
```

#### Save to txt

To save the contents of a previously encrypted file as plaintext run

```bash
python main.py -de crypted_lore.txt lore_key.txt decrypted_lore.txt
```

## Usage of diffy.py

---

**Attention**:
While this feature is fully functioning it is underdevelopted. For Diffie-Hellman key-exchanges to be considered secure the underlying prime numbers *should* be longer (2048+ bits) than the ones implemented in this project (~64 bits). 

### Run as host:

```bash
python diffie.py h
```

### Run as client:

```bash
python diffie.py c
```

## Developer Comment

---

*Section yet to be written...*
