import os
import sys

from cryptology import utils
import cryptology.aes.pyaes as pyaes
import cryptology.prim_roots.primitive_roots as pr

def main():
    print(dir(pyaes))
    print(dir(pr))
    print(dir(utils))

    inpath = os.path.abspath(sys.argv[1])
    outpath = os.path.abspath(sys.argv[2])

    print(inpath)
    print(outpath)

if __name__ == "__main__":
    main()
