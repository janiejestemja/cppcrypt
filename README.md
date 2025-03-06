## Installation

--- 


```bash
python setup.py build_ext --inplace
```

## Usage

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