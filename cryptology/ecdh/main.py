from random import randint
import elliptic_curves as ec
from hashlib import sha256
from hmac import new as hmac_new

def main():
    secp256k1 = ec.EllipticCurve(0, 7, 0xFFFFFFFF_FFFFFFFF_FFFFFFFF_FFFFFFFF_FFFFFFFF_FFFFFFFF_FFFFFFFE_FFFFFC2F)
    G = ec.ECPoint(secp256k1, 0x79BE667E_F9DCBBAC_55A06295_CE870B07_029BFCDB_2DCE28D9_59F2815B_16F81798, 
               0x483ADA77_26A3C465_5DA4FBFC_0E1108A8_FD17B448_A6855419_9C47D08F_FB10D4B8)

    a_pri, a_pub = gen_keypair(secp256k1, G)
    b_pri, b_pub = gen_keypair(secp256k1, G)

    asecret = b_pub.multiply(a_pri)
    bsecret = a_pub.multiply(b_pri)

    print("Key: ")
    print(hkdf_extract_expand(asecret))

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

if __name__ == "__main__":
    main()
