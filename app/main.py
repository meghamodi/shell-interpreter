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
        elif userarg[:4] == "pwd":
            print(os.getcwd())
        elif userarg[:2] == "cd":
                path= userarg[2:].strip()
                if os.path.exists(path):
                    os.chdir(path)
                elif path == './':
                    continue
                elif path == '../':
                    os.chdir('..')
                elif path.startswith('./'):
                    os.chdir(path)
                elif path == '~':
                    os.chdir('/')
                else:
                    print(f"{userarg[:2]}:{userarg[2:]}: No such file or directory")


        elif userarg[:5] == "type ":
            if userarg[5:] == "echo" or userarg[5:] == "exit" or userarg[5:] == "type" or userarg[5:]=="pwd" :
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
                    print(f"{cmd}: not found")
        else:
                cmd = userarg.split()
                executable = cmd[0]
                args = cmd[1:]
                found = False
            
                for dir in PATH.split(":"):
                    # change dir, then search for the command, if not go to next dir
                    try:
                        entries= os.listdir(dir)
                        
                        if executable in entries:
                            fullPath = os.path.join(dir,executable)
                            if os.access(fullPath,os.X_OK):
                                found = True
                                pid=os.fork()
                                if pid ==0:
                                    os.execv(fullPath,[executable]+ args)
                                else:
                                    os.wait()
                                break
                            
                    except:
                        continue         
        
                if not found:
                    print(f"{executable}: not found")
       
        
   

if __name__ == "__main__":
    main()
