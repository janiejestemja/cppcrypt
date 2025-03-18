from aes.pyaes import key_expansion, aes_encrypt, aes_decrypt

def save_files(file_name : str, crypt_name : str, key_name : str):
    key = bytes( 
        [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f]
    )
    round_keys = key_expansion(key)   

    # Encryption
    states = str_to_states(read_text(filename=file_name))
    cipherstates = []
    for state in states:
        cipherstates.append(aes_encrypt(state, round_keys))

    # Save encrypted file
    save_crypt(crypt_name, cipherstates)

    with open(key_name, "w") as f:
        for ele in key:
            f.write(str(ele) + "\n")

def load_files(crypt_name : str, key_name : str) -> str:
    loaded_key = []
    with open(key_name) as f:
        reader = f.readlines()
        loaded_key = [int(key.strip("\n")) for key in reader]

    loaded_keys = key_expansion(loaded_key)
    # Load encrypted file
    text_fromf = read_crypt(crypt_name)

    # Decryption
    decipheredstates = [aes_decrypt(state, loaded_keys) for state in text_fromf]

    return states_to_text(decipheredstates)

def read_text(filename="lore.txt"):
    text = ""
    with open(filename) as f:
        reader = f.read()
        text = reader

    return text

def save_crypt(filename, cipherstates):
    state_strs = []
    for state in cipherstates:
        row_strs = []
        for row in state:
            row_str = ",".join(str(ele) for ele in row)
            row_strs.append(row_str)
        state_str = ";".join(row for row in row_strs)
        state_strs.append(state_str)

    with open(filename, "w") as f:
        for state_str in state_strs:
            f.write(state_str + "\n")

def read_crypt(filename):
    # Reading from file
    from_file = []
    with open(filename) as f:
        reader = f.readlines()
        for line in reader:
            from_file.append(line.strip("\n"))

    text_fromf = []
    for line in from_file:
        row_strs = line.split(";")

        state = []
        for row_str in row_strs:
            row = [int(ele) for ele in row_str.split(",")]
            state.append(row)
        text_fromf.append(state)

    return text_fromf


def str_to_states(text : str) -> list:
    const = 16
    hex_text = []

    for char in text:
        if ord(char) < 0 or ord(char) > 254:
            hex_text.append(hex(ord("?")))
        else:
            hex_text.append(hex(ord(char)))
            
    for _ in range(const - (len(text) % const)):
        hex_text.append(hex(ord(" ")))
        
    states = []

    hex_len = len(hex_text)
    
    for i in range(0, hex_len, 16):
        state = []
        
        for j in range(4):
            row = []
            
            for k in range(4):
                row.append(int(hex_text[i + 4 * j + k], 16))
            state.append(row)
        states.append(state)

    return states

def states_to_text(states : list) -> str:
    txt_from_hex = ""
    
    for i, state in enumerate(states):
        for j, row in enumerate(state):
            for k, element in enumerate(row):
                txt_from_hex = txt_from_hex + chr(int(states[i][j][k]))

    return txt_from_hex
