# Return-to-libc Attack Lab

## Task 3: Launching the Attack

Make always sure that you run the following commands to disable the address randomization countermeasure enable by default in every OS, and use the vulnerable shell zsh as default one:

```console
$ sudo /sbin/sysctl -w kernel.randomize_va_space=0
$ sudo ln -sf /bin/zsh /bin/sh
```

*Attack variation 1: Is the exit() function really necessary? Please try your attack without including the address of this function in badfile. Run your attack again, report and explain your observations.*

For this kind of attack, the exit function is not useful. Indeed, running the attack without its address in the badfile doesn't change the behaviour of the program.

*Attack variation 2: After your attack is successful, change the file name of retlib to a different name, making sure that the length of the new file name is different. For example, you can change it to newretlib. Repeat the attack (without changing the content of badfile). Will your attack succeed or not? If it does not succeed, explain why.*

Changing the name of the executable "retlib" to "newretlib", the attack doesn't succeed and the output is the following one:

```console
Address of input[] inside main():  0xffffc4d0
Input size: 300
Address of buffer[] inside bof():  0xffffc4a0
Frame Pointer value inside bof():  0xffffc4b8
zsh:1: command not found: h
Errore di segmentazione (core dump creato)
```

This happens because MYSHELL is passed to the vulnerable program as an environment variable, which is stored on the stack. But the address of MYSHELL environment variable is sensitive to the length of the program name, because the program name is stored on the stack, so changing the lenght of the program name implies that the address of MYSHELL shifts.

## Task 4 (Optional): Defeat Shell’s countermeasure

Make always sure that you use the not vulnerable bash or dash shell as default one:

```console
$ sudo ln -sf /bin/bash /bin/sh
```

1. Because after running the execve function prologue, the system arguments are located 8 bytes after the EBP register, the address of "/bin/sh" needs to be stored at this location. The address of "/bin/sh" is stored on the stack using an environment variable I created, and I can obtain its address printing it with prtenv program. The difference between the frame pointer address and the buffer[] address is 80. In addition to this, you have also to consider the 4 bytes where base pointer is located. Thus, the location of the return address is 80(buffer) + 4(base pointer)=84 bytes away, and the location of the arguments is 80(buffer) + 4(base pointer) + 8(arguments)=92 bytes away.

2. The address of execv can be printed using gdb peda on the vulnerable program, and I put it 4 bytes after EBP, substituting the return address.

3. The exit address can be printed using gdb peda on the vulnerable program. I put it 8 bytes after EBP exactly below the address of the argv inserted in point one, subsituting the return address used after when the execv function is called, so that when the execv epilogue is executed it returns to the exit() function.

4. I compute the difference between the main stack frame and the bof stack frame in order to store and recover the arguments of execv inside argv. Let's call this difference "frames_gap".

5. I put as a further argument on the stack (other than the address of "/bin/sh") the address of the argv array, which points to the arguments inside the main stack frame that will be placed at "address of input[] inside main() + frames_gap" location. Indeed, execv takes in input two parameters: the command and the argv[] array which contains further options. Since argv[] is an argument of execv (as the address of "/bin/sh"), I place this above this latter argument, 12 bytes after the EBP register (that means 80(buffer) + 4(base pointer) + 12(arguments)=96 bytes away).

6. In order to recover the values inside argv[], I have to store them on the stack. So, at distance frames_gap away from the buffer, I put first the pathname address "/bin/sh" as argv[0] recovered as in point 1, 4 bytes later I put the address "-p" as argv[1] also stored inside an environment variable that I created and I retrive its address using prtenv program, and finally 4 bytes later the four bytes that contain 0x0 to indicate the end of the string as argv[2].

## Task 5 (Optional): Return-Oriented Programming

Reusing the previous code, I simply add this lines:

```c
F = (ebp + 4) - BUF
foo_addr = 0x565562b0       # The address of foo()
i = 0
while i < 4*FOOs:
    content[F+i : F+i+4] = (foo_addr).to_bytes(4,byteorder='little')
    i += 4
ebp = ebp + i
...
```
I recover the foo address using gdb peda. Then, starting from the first return address at location EBP + 4, I write in all the 4 bytes stack cells the foo address for 10 times, corresponding to the 40 bytes after the EBP. Then, I update the value of EBP considering all the inserted return addresses, and reuse the same exactly code of the previous challenge.