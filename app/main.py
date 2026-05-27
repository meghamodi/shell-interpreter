import sys


def main():
    sys.stdout.write("$ ")
    userarg = input()
    print(f"{userarg}: command not found")


if __name__ == "__main__":
    main()
