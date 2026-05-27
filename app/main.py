import sys


def main():
    while True:
        sys.stdout.write("$ ")
        userarg = input()
        if userarg == "exit":
            break
        elif userarg[:5] == "echo ":
            print(userarg[5:])
        elif userarg[:5] == "type ":
            if userarg[5:] == "echo" or userarg[5:] == "exit" :
                print(f"{userarg[5:]} is a shell builtin")
            else:
                print(f"{userarg[5:]}: not found")
        else:
            print(f"{userarg}: command not found")

if __name__ == "__main__":
    main()
