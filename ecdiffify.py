import sys
from random import choice, randint

from cryptology.utils import read_text
from cryptology.ec_utils import client, server

def main():
    ipvfour = input("IPv4: ")
    if ipvfour == "":
        ipvfour = "127.0.0.100"

    portnumber = input("Port: ")

    if portnumber == "":
        portnumber = 12345

    else:
        try:
            portnumber = int(portnumber)
        except TypeError:
            sys.exit("Portnumber not a number")
    

    if sys.argv[1] == "h":
        infile = input("File to send: ")

        if infile != "":
            text = read_text(infile)
        else:
            text = read_text()
        server(ipvfour, portnumber, text)

    elif sys.argv[1] == "c":
        client(ipvfour, portnumber)

if __name__ == "__main__":
    main()
