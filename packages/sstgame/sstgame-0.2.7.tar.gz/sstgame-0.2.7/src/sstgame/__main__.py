import argparse
from src import sstgame

def main():
    parser = argparse.ArgumentParser(description="Generate a madlib story")
    parser.add_argument("--file", required=False, help="Path to the madlib input file")

    args = parser.parse_args()
    file_path = args.file

    madlib_result = sstgame.madlib.madlib(file_path)
    print(madlib_result)

if __name__ == "__main__":
    main()