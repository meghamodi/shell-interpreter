import sys


def main():
    while True:
        sys.stdout.write("$ ")
        userarg = input()
        if userarg == "exit":
            break
        elif userarg[:5] == "echo ":
            print(userarg[5:])
          
        else:
            print(f"{userarg}: command not found")

if __name__ == "__main__":
    main()
