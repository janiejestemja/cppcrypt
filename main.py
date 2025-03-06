import sys

from utils import load_files, save_files

def main():
    if len(sys.argv) != 5:
        sys.exit("Missing cla")


    # Encryption
    if sys.argv[1] == "-en":
        file_name = sys.argv[2]
        crypt_name = sys.argv[3]
        key_name = sys.argv[4]
        save_files(file_name=file_name, crypt_name=crypt_name, key_name=key_name)

    # Decryption
    elif sys.argv[1] == "-de":
        crypt_name = sys.argv[2]
        key_name = sys.argv[3]
        file_name = sys.argv[4]

        # Priting 
        if file_name == "-p":
            print(load_files(crypt_name=crypt_name, key_name=key_name))

        # Saving to file
        else:
            with open(file_name, "w") as f:
                f.write(load_files(crypt_name=crypt_name, key_name=key_name))

if __name__ == "__main__":
    main()
