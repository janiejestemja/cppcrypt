import sys

from utils import load_files, save_files

def main():
    if len(sys.argv) != 4:
        sys.exit("Missing cla")


    if sys.argv[1] == "-en":
        filename = sys.argv[2]
        cryptname = sys.argv[3]
        save_files(filename=filename, cryptname=cryptname)

    elif sys.argv[1] == "-de":
        cryptname = sys.argv[2]
        filename = sys.argv[3]
        with open(filename, "w") as f:
            f.write(load_files(cryptname=cryptname))

if __name__ == "__main__":
    main()
