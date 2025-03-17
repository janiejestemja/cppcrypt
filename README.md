# Python module for Cryptography 
#### written in C++
---

## Description

---

This is a learning project about the Diffie-Hellman key-exchange and advanced ecryption standard (AES). 

## Directory Structure

---

```plaintext
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

To install the necessary third party dependencies run

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

```bash
python main.py -de crypted_lore.txt lore_key.txt -p
```

#### Save to txt

```bash
python main.py -de crypted_lore.txt lore_key.txt decrypted_lore.txt
```
