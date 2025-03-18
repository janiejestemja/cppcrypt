import sys
from random import choice, randint

from cryptology.utils import client, server, read_text

def main():
    if sys.argv[1] == "h":
        infile = input("File to send: ")
        if infile != "":
            text = read_text(infile)
        else:
            text = read_text()
        server(text)
    elif sys.argv[1] == "c":
        client()

if __name__ == "__main__":
    main()
