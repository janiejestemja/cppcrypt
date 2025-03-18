import socket
from random import choice, randint
from time import sleep
from aes.pyaes import key_expansion, aes_encrypt, aes_decrypt
from prim_roots import primitive_roots as pr

primes = [
        11111111111111111011,
        11111313171722335577,
        11138479445180240497,
        11281963036964038421,
        11976506590973322187,
        12345678901234567891,
        12345678910987654321,
        12797382490434158663,
        12904149405941903143,
        13080048459073205527,
        13169525310647365859,
        13315146811210211749,
        13337777797999979999,
        13337779797779999999,
        13464654573299691533,
        14400146411488415129,
        15021025033035039049,
        15396334245663786197,
        16808980088116168811,
        17131175322357111317,
        17625750738756291797,
        18446744065119617029,
        18446744069414584321,
]

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


def read_text(filename="lore.txt"):
    text = ""
    with open(filename) as f:
        reader = f.read()
        text = reader

    return text

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


# Generate public variables on the server
def generate_public():
    prime = choice(primes)
    prim_root = pr.find_primitive_roots(prime)[-1]
    a = randint(3, 99)

    big_a = pow(prim_root, a) % prime

    return (a, big_a, prime, prim_root)

# Calculate shared secret on client
def client_secret(big_a, prime, prim_root):
    b = randint(3, 99)
    big_b = pow(prim_root, b) % prime

    shared_secret = pow(big_a, b) % prime

    return (b, big_b, shared_secret)

# Calculate shared secret on server
def server_secret(a, big_b, prime):
    shared_secret = pow(big_b, a) % prime

    return shared_secret

def server(text):
    a, big_a, prime, prim_root = generate_public()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 12345))
    server_socket.listen()
    print("Server is listening...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        # Send public variables to client
        client_socket.send(bytes(str(big_a).encode()))
        sleep(0.01)
        client_socket.send(bytes(str(prime).encode()))
        sleep(0.01)
        client_socket.send(bytes(str(prim_root).encode()))
        sleep(0.01)
        client_socket.send(bytes(str("exit()").encode()))
        print("Public variables send")

        # Recieve public variable
        big_b = int(client_socket.recv(1024).decode())
        # Calculate shared secret
        shared_secret = server_secret(a, big_b, prime)

        # Expand Key
        round_keys = key_expansion(bytes(str(shared_secret)[:16].encode()))

        # Encrypt and send text
        states = str_to_states(text)
        cipherstates = [aes_encrypt(state, round_keys) for state in states]

        for cipherstate in cipherstates:
            for row in cipherstate:
                for ele in row:
                    client_socket.send(bytes(str(ele).encode()))
                    sleep(0.01)

        client_socket.send(bytes(str("exit()").encode()))

        client_socket.close()
        server_socket.close()
        break

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 12345))

    # Recieve public variables from server
    public_variables = []
    while True:
        message = client_socket.recv(1024)
        if message.decode() == "exit()":
            break
        else:
            public_variables.append(int(message.decode()))

    # Calculate private var, public var and shared secret
    b, big_b, shared_secret = client_secret(*public_variables)
    round_keys = key_expansion(bytes(str(shared_secret)[:16].encode()))

    # Send public var
    client_socket.send(bytes(str(big_b).encode()))

    # Recieve and decipher text
    i = 0
    j = 0
    row = []
    cipherstate = []
    cipherstates = []
    while True:
        message = client_socket.recv(1024)
        if message.decode() == "exit()":
            break
        elif message.decode() == "":
            continue
        else:
            row.append(int(message.decode()))
            j += 1
            if j > 3:
                cipherstate.append(row)
                i += 1
                row = []
                j = 0
            if i > 3:
                cipherstates.append(cipherstate)
                cipherstate = []
                i = 0

    states = [aes_decrypt(cipherstate, round_keys) for cipherstate in cipherstates]
    print(states_to_text(states))

    client_socket.close()
