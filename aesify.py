import sys
from getpass import getpass

from cryptology.utils import check_passkey, load_file, save_file

def main():
    if len(sys.argv) != 4:
        sys.exit("Missing cla")


    default_passkey = "0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f"
    # Encryption
    if sys.argv[1] == "-en":
        file_name = sys.argv[2]
        crypt_name = sys.argv[3]
        passkey = getpass()
        # Default passkey
        if passkey == "":
            passkey = default_passkey
        elif check_passkey(passkey) == False:
            sys.exit("Passkey check failed")

        save_file(file_name=file_name, crypt_name=crypt_name, passkey=passkey)

    # Decryption
    elif sys.argv[1] == "-de":
        crypt_name = sys.argv[2]
        file_name = sys.argv[3]

        passkey = getpass("Passkey: ")
        if passkey == "":
            passkey = default_passkey

        elif check_passkey(passkey) == False:
            sys.exit("Passkey check failed")

        # Priting 
        if file_name == "-p":
            print(load_file(crypt_name=crypt_name, passkey=passkey))

        # Saving to file
        else:
            with open(file_name, "w") as f:
                f.write(load_file(crypt_name=crypt_name, passkey=passkey))


if __name__ == "__main__":
    main()
