import sys
import os

def main():
    PATH = os.environ["PATH"]
    while True:
        sys.stdout.write("$ ")
        userarg = input()
        
        if userarg == "exit":
            break
        elif userarg[:5] == "echo ":
            print(userarg[5:])
        elif userarg[:5] == "type ":
            if userarg[5:] == "echo" or userarg[5:] == "exit" or userarg[5:] == "type" :
                print(f"{userarg[5:]} is a shell builtin")
                
            else:
                cmd = userarg[5:]
                for dir in PATH.split(":"):
                    # change dir, then search for the command, if not go to next dir
                    try:
                        entries= os.listdir(dir)
                        if cmd in entries:
                            fullPath = os.path.join(dir,cmd)
                            if os.access(fullPath,os.X_OK):
                                print(f"{cmd} is {fullPath}")
                                break
                        
                    except:
                        continue
                else:
                    # only runs if loop exhausted all dirs without break
                    print(f"{cmd}: not found")

        else:
            print(f"{userarg}: command not found")

if __name__ == "__main__":
    main()
