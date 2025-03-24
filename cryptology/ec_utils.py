import socket
from random import randint
from time import sleep
from hashlib import sha256
from hmac import new as hmac_new
from pyaes import key_expansion, aes_decrypt, aes_encrypt
from cryptology.utils import str_to_states, states_to_text

from .ecdh import elliptic_curves as ec


secp256k1 = ec.EllipticCurve(
        0, 
        7, 
        0xFFFFFFFF_FFFFFFFF_FFFFFFFF_FFFFFFFF_FFFFFFFF_FFFFFFFF_FFFFFFFE_FFFFFC2F
)
G = ec.ECPoint(
        secp256k1, 
        0x79BE667E_F9DCBBAC_55A06295_CE870B07_029BFCDB_2DCE28D9_59F2815B_16F81798, 
        0x483ADA77_26A3C465_5DA4FBFC_0E1108A8_FD17B448_A6855419_9C47D08F_FB10D4B8
)

def hkdf_extract_expand(shared_secret, salt=b"some_salt", info=b"AES key"):
    prk = hmac_new(salt, shared_secret.x.to_bytes(32, "big"), sha256).digest()
    okm = hmac_new(prk, info + b"\x01", sha256).digest()
    return [bit for bit in okm[:16]]

def gen_keypair(curve, G):
    pri_key = randint(1, curve.p - 1)
    pub_key = G.multiply(pri_key)

    # Recursion if pub_key is point at inf
    if pub_key == ec.ECPoint(curve, None, None):
        return gen_keypair(curve, G)

    return pri_key, pub_key

def server(ipvfour, portnumber, text : str, curve=secp256k1, G=G):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ipvfour, portnumber))
    server_socket.listen()
    print("Server is listening...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        a_pri, a_pub = gen_keypair(curve, G)

        # Send public variables to client
        client_socket.send(bytes(str(a_pub.x).encode()))
        sleep(0.01)
        client_socket.send(bytes(str(a_pub.y).encode()))
        sleep(0.01)
        client_socket.send(bytes(str("exit()").encode()))
        print("Public variables send")

        # Recieve public variable from client
        pub_vars = []
        while True:
            message = client_socket.recv(1024)
            if message.decode() == "exit()":
                break
            else:
                pub_vars.append(message.decode())


        b_pub = ec.ECPoint(curve, int(pub_vars[0]), int(pub_vars[1]))
        shared_secret = hkdf_extract_expand(b_pub.multiply(a_pri))

        # Expand Key
        round_keys = key_expansion(shared_secret)

        # Encrypt and send text
        states = str_to_states(text)
        cipherstates = [aes_encrypt(state, round_keys) for state in states]

        print("Sending ciphertext...")
        for cipherstate in cipherstates:
            for row in cipherstate:
                for ele in row:
                    client_socket.send(bytes(str(ele).encode()))
                    sleep(0.01)

        client_socket.send(bytes(str("exit()").encode()))

        print("Closing connection")
        client_socket.close()
        server_socket.close()
        break

def client(ipvfour : str, portnumber: int, curve=secp256k1, G=G):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ipvfour, portnumber))

    # Recieve public variable from server
    pub_vars = []
    while True:
        message = client_socket.recv(1024)
        if message.decode() == "exit()":
            break
        else:
            pub_vars.append(message.decode())

    a_pub = ec.ECPoint(curve, int(pub_vars[0]), int(pub_vars[1]))

    b_pri, b_pub = gen_keypair(curve, G)
    shared_secret = hkdf_extract_expand(a_pub.multiply(b_pri))

    round_keys = key_expansion(shared_secret)

    # Send public variables to server
    client_socket.send(bytes(str(b_pub.x).encode()))
    sleep(0.01)
    client_socket.send(bytes(str(b_pub.y).encode()))
    sleep(0.01)
    client_socket.send(bytes(str("exit()").encode()))
    print("Public variables send")


    print("Recieving cipher...")
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

    print("Ciphertext recieved...")
    states = [aes_decrypt(cipherstate, round_keys) for cipherstate in cipherstates]
    print(states_to_text(states))

    client_socket.close()
