import socket
import sys
from time import sleep
from random import choice, randint

from prim_roots import primitive_roots as pr
from aes.pyaes import key_expansion, aes_encrypt, aes_decrypt

def main():
    if sys.argv[1] == "h":
        server()
    elif sys.argv[1] == "c":
        client()

state = [
        [0x00, 0x01, 0x02, 0x03],
        [0x10, 0x11, 0x12, 0x13],
        [0x20, 0x21, 0x22, 0x23],
        [0x30, 0x31, 0x32, 0x33]
]

primes = [
        2015121110987654321,
        5555555555555555533,
        7393913311133193937,
        8888888897888888899,
]

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
    a, big_a, prime, prim_root = generate_public()
    print(a, big_a, prime, prim_root, sep= " : ")
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

        big_b = int(client_socket.recv(1024).decode())
        shared_secret = server_secret(a, big_b, prime)
        print(shared_secret)

        round_keys = key_expansion(bytes(str(shared_secret)[:16].encode()))
        cipherstate = aes_encrypt(state, round_keys)
        print(cipherstate)

        for row in cipherstate:
            for ele in row:
                client_socket.send(bytes(str(ele).encode()))
                sleep(0.1)

        client_socket.send(bytes(str("exit()").encode()))
        sleep(0.1)

        print(round_keys)

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


    b, big_b, shared_secret = client_secret(*public_variables)
    client_socket.send(bytes(str(big_b).encode()))
    print(shared_secret)

    ciphers = []
    while True:
        message = client_socket.recv(1024)
        if message.decode() == "exit()":
            break
        else:
            ciphers.append(int(message.decode()))

    cipherstate = []
    for i in range(4):
        row = []
        for j in range(4):
            row.append(ciphers[4 * i + j])
        cipherstate.append(row)

    for row in cipherstate:
        print(row)

    round_keys = key_expansion(bytes(str(shared_secret)[:16].encode()))
    print(round_keys)
    client_socket.close()

if __name__ == "__main__":
    main()
