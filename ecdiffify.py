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

def validate(ip):
    """ 
    Simplified validation of IPv4 Adresses.

    Args:
        ip (str): A str potentially containing valid IPv4 Adress.
    
    Returns:
        bool: Result of validation.
    """

    # trying to extract substrings into a list
    try: 
        elements = list(ip.split("."))

    # handling exception
    except (ValueError, TypeError):
        return False

    else: 
        # trying to typeforce elements in the list
        try:
            numb3rs = list()

            for element in elements:
                numb3rs.append(int(element))

        # handling exception
        except ValueError:
            return False 

        else:
            # checking for correct length
            if len(numb3rs) == 4:
                # Current state
                state = True
                # checking accepted ranges for numbers in the adress
                for numb3r in numb3rs:
                    if numb3r > 255:
                        state = False

                    elif numb3r < 0:
                        state = False

                    else:
                        continue

                return state

            else:
                # otherwise returning false
                return False

if __name__ == "__main__":
    main()
