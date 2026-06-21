import sys
import os
import shlex
import subprocess
from pathlib import Path

def parse_redirect(args):
    operator= [">","1>"]
    matchOperator= next((x for x in operator if x in args),None)

    if matchOperator is None:
        return args,None
    operIndex = args.index(matchOperator)
    content = args[:operIndex]
    output_file = args[operIndex+1]
    
    return content, output_file

def write_output(text,file):
    if file:
        with open(file,'w') as f:
            f.write(text + "\n")
    else:
        print(text)
        

def main():
    PATH = os.environ["PATH"]
    while True:
        sys.stdout.write("$ ")
        userarg = input()
        
        if userarg == "exit":
            break
        
        elif userarg[:5] == "echo ":

            s= userarg[5:]
            args = shlex.split(s)
            
            args,output_file = parse_redirect(args)
            write_output(' '.join(args),output_file)


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
                    homeDir= os.getenv('HOME')
                    os.chdir(homeDir)
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
                cmd = shlex.split(userarg)
                cmd,output_file = parse_redirect(cmd)
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
                                    if output_file:
                                        fd = os.open(output_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
                                        os.dup2(fd, 1)   # redirect stdout (fd 1) to the file
                                        os.close(fd)
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
