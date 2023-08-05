
Perform is for calling processes from python in a simple and easy way.  Each program is added to the perform module as a function that returns the stdout printed by the program.

Examples:
To call a normal program that whose name doesn't contain symbols:
    stdout = perform.ls()

To pass arguments to a program:
    stdout = perform.git("ls-files", "-m")

To call a program that contains symbols in its name:
    stdout = perform._("pip2.7", "install", "perform")

To get stderr from a program:
    try:
        perform.git("asdad")
    except Exception as e:
        print(str(e))

To call a command in the shell:
    print(perform._("ls | grep 'py'", shell=True))


