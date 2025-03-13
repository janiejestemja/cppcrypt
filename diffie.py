import socket
import sys
from time import sleep
from random import choice, randint

from prim_roots import primitive_roots as pr
from aes.pyaes import key_expansion, aes_encrypt, aes_decrypt
from utils import states_to_text, str_to_states, read_text

def main():
    if sys.argv[1] == "h":
        server()
    elif sys.argv[1] == "c":
        client()


primes = [
        2015121110987654321,
        5555555555555555533,
        7393913311133193937,
        8888888897888888899,
]

text = read_text()

def generate_public():
    prime = primes[0]
    prim_root = choice(pr.find_primitive_roots(prime))
    a = randint(3, 13)

    big_a = pow(prim_root, a)

    return (a, big_a, prime, prim_root)

def client_secret(big_a, prime, prim_root):
    b = randint(13, 23)
    big_b = pow(prim_root, b)

    shared_secret = pow(big_a, b) % prime

    return (b, big_b, shared_secret)

def server_secret(a, big_b, prime):
    shared_secret = pow(big_b, a) % prime

    return shared_secret

def server():
    state = [
            [0x00, 0x01, 0x02, 0x03],
            [0x10, 0x11, 0x12, 0x13],
            [0x20, 0x21, 0x22, 0x23],
            [0x30, 0x31, 0x32, 0x33]
    ]
    a, big_a, prime, prim_root = generate_public()
    print(big_a, prime, prim_root, sep= " : ")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 12345))
    server_socket.listen()
    print("Server is listening...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        # Send public variables to client
        client_socket.send(bytes(str(big_a).encode()))
        sleep(0.1)
        client_socket.send(bytes(str(prime).encode()))
        sleep(0.1)
        client_socket.send(bytes(str(prim_root).encode()))
        sleep(0.1)
        client_socket.send(bytes(str("exit()").encode()))
        print("Public variables send")

        # Recieve public variable
        big_b = int(client_socket.recv(1024).decode())
        # Calculate shared secret
        shared_secret = server_secret(a, big_b, prime)
        print(shared_secret)

        # Expand Key
        round_keys = key_expansion(bytes(str(shared_secret)[:16].encode()))
        # Encrypt one state
        cipherstate = aes_encrypt(state, round_keys)
        # Send states elements
        for row in cipherstate:
            for ele in row:
                client_socket.send(bytes(str(ele).encode()))
                sleep(0.1)
        client_socket.send(bytes(str("exit()").encode()))
        sleep(0.1)

        states = str_to_states(text)
        cipherstates = [aes_encrypt(state, round_keys) for state in states]
        for cipherstate in cipherstates:
            for row in cipherstate:
                for ele in row:
                    client_socket.send(bytes(str(ele).encode()))
                    sleep(0.1)
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
        print(f"Recieved: {message.decode()}")


    # Calculate private var, public var and shared secret
    b, big_b, shared_secret = client_secret(*public_variables)
    print(shared_secret)
    round_keys = key_expansion(bytes(str(shared_secret)[:16].encode()))

    # Send public var
    client_socket.send(bytes(str(big_b).encode()))

    # Recieve one ciphered state
    ciphers = []
    while True:
        message = client_socket.recv(1024)
        if message.decode() == "exit()":
            break
        else:
            ciphers.append(int(message.decode()))

    # Reformat recieved ciphered state
    cipherstate = []
    for i in range(4):
        row = []
        for j in range(4):
            row.append(ciphers[4 * i + j])
        cipherstate.append(row)

    # Decipher state
    deciphered_state = aes_decrypt(cipherstate, round_keys)

    # Decipher text
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

if __name__ == "__main__":
    main()
