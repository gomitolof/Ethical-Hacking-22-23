# Task 1.b. Eliminating Zeros from the Code

* *If we want to assign zero to eax, we can use “mov eax, 0”, but doing so, we will get a zero in the machine code. A typical way to solve this problem is to use “xor eax, eax”. Please explain why this would work.*

The assembly code xor eax, eax perform the xor operation between the register eax with itself, and this is equal to zero. Finally, store the result in the register eax.

* *If we want to store 0x00000099 to eax. We cannot just use mov eax, 0x99, because the second operand is actually 0x00000099, which contains three zeros. To solve this problem, we can first set eax to zero, and then assign a one-byte number 0x99 to the al register, which is the least significant 8 bits of the eax register.*

* *Another way is to use shift. In the following code, first 0x237A7978 is assigned to ebx. The ASCII values for x, y, z, and # are 0x78, 0x79, 0x7a, 0x23, respectively. Because most Intel CPUs use the small-Endian byte order, the least significant byte is the one stored at the lower address (i.e., the character x), so the number presented by xyz# is actually 0x237A7978. You can see this when you dissemble the code using objdump. After assigning the number to ebx, we shift this register to the left for 8 bits, so the most significant byte 0x23 will be pushed out and discarded. We then shift the register to the right for 8 bits, so the most significant byte will be filledwith 0x00. After that, ebx will contain 0x007A7978, which is equivalent to “xyzn\0”, i.e., the last byte of this string becomes zero.*

* *Task. In Line [1] of the shellcode mysh.s, we push “//sh” into the stack. Actually, we just want to push “/sh” into the stack, but the push instruction has to push a 32-bit number. Therefore, we add a redundant / at the beginning; for the OS, this is equivalent to just one single /. For this task, we will use the shellcode to execute /bin/bash, which has 9 bytes in the command string (10 bytes if counting the zero at the end). Typically, to push this string to the stack, we need to make the length multiple of 4, so we would convert the string to /bin////bash. However, for this task, you are not allowed to add any redundant / to the string, i.e., the length of the command must be 9 bytes (/bin/bash). Please demonstrate how you can do that. In addition to showing that you can get a bash shell, you also need to show that there is no zero in your code.*

In order to solve that, I modify the previous shellcode basic x86 shellcode mysh.s pushing /bin/bash string to the stack in the following way:

```c
...
    xor  eax, eax 
    push eax          ; Use 0 to terminate the string
    mov   al, 0x68    ; eax = 0x00000068
    push eax
    push "/bas"
    push "/bin"
...
```

We first set eax to zero, push it to the stack to terminate the string, and then assign one-byte 0x68 (that correspond to the "h" character) to the al register, which is the least significant 8 bits of the eax register. Finally, the remaining 8 characters are pushed normally to the stack each 4 bytes.

# Task 1.c. Providing Arguments for System Calls

First, we store the arguments strings to the stack terminating each argument with a 0 using "xor eax, eax". For the strings of length 2 bytes, we set eax to zero and assign the two bytes to the al and ah registers. Then, we push to the stack the eax register.

After saving each argument, we store its address on the variables ebx, ecx and edx using the command "mov  edx, esp", so we can use them later to push each argument's address on the stack.

# Task 1.d. Providing Environment Variables for execve()

Similar procedure as before, except that now:

* We use the shif left and shif right approach to complete the 1 bytes string "4###" storing it on the edx register and pushing it on the stack.

* We cannot use the ebx and ecx registers since they have the string address and the argv address respectively. In alternative, we use esi and edi registers.

# Task 2: Using Code Segment

1. Please provide a detailed explanation for each line of the code in mysh2.s, starting from the line labeled one. Please explain why this code would successfully execute the /bin/sh program, how the argv[] array is constructed, etc.

* "pop ebx" instruction actually get the address of the string '/bin/sh*AAAABBBB' and save it to the ebx register.

* "xor eax, eax" store the result of the xor operation between eax register and itself, that is zero, in the eax register. So now: "eax = 0x00000000".

* "mov [ebx+7], al" substitute the * inside the string with a zero to end the first string, so we have that ebx points to "/bin/sh0AAAABBBB".

* "mov [ebx+8], ebx" substitute the placeholder AAAA inside the string with the string address, so argv[0] points "/bin//sh". So ebx register points to "/bin/sh0<string-addr>BBBB".

* "mov [ebx+12], eax" substitute the placeholder BBBB inside the string with zeros, so argv[1] = 0. Now ebx register points to "/bin/sh0<string-addr>0000".

* "lea ecx, [ebx+8]" load the address of argv[] in the ecx register.

* "xor edx, edx" store the result of the xor operation between edx register and itself, that is zero, in the edx register. So now: "edx = 0x00000000". This indicates that there aren't environment variables.

* "mov al,  0x0b" assign a one-byte number 0x0b (that is equal to 11, the number related to the execve function) to the al register, which is the least significant 8 bits of the eax register. So now "eax = 0x0000000b".

* "int 0x80" invokes the execve function with the passed arguments.

* Actually, this shellcode mysh2.s inoke a shell as mysh.s does, but instead of solving the data address problem dynamically constructing all the necessary data structures on the stack, so their addresses can be obtained from the stack pointer esp, in this approach mush2.s stores the data in the code region and its address is obtained via the function call mechanism. When the call instruction is executed, the address of the data is treated as the return address, and is pushed into the stack.

2. Please use the technique from mysh2.s to implement a new shellcode, so it executes /usr/bin/env, and it prints out the following environment variables:

```console
a=11
b=22
```

* The string stored by the db instruction is:

```c
db '/usr/bin/env*a=11*b=22**AAAABBBBCCCCDDDDEEEE'
```

* The asterisks separate the strings, except the last one which is used to fill the gap of 4 bytes in the last memory cell that separate the strings from the placeholders.

* As before, we need to substitute the asterisks with zeros, and we can do that using the xor function of eax with itself, and storing the al register value inside the string positions that contain the asterisk.

* Construct the argument array argv[]: the same as before, just the addresses change.

* Construct the environment argument array env[]: using the ebx register we substitute the CCCC with the address of "a=11" so env[0] points "a=11", DDDD with the address of "b=22" so env[1] points "b=22" and CCCC with zeros so env[2] = 0. Finally, we load in the edx register the address of env[] memorized in [ebx+32].

* The rest remains exactly the same as before.

# Task 3: Writing 64-bit Shellcode (optional)

*Repeat Task 1.b for this 64-bit shellcode. Namely, instead of executing “/bin/sh”, we need to execute “/bin/bash”, and we are not allowed to use any redundant / in the command string, i.e., the length of the command must be 9 bytes(/bin/bash). Please demonstrate how you can do that. In addition to showing that you can get a bash shell, you also need to show that there is no zero in your code.*

It is the same thing as Task 1.b, except that now we use other registers. In particular, to insert zeros without explicitly writing them, rdx and dl regiters are used. We store the remaining character "h" inside the dl register and then push rdx in the stack, avoiding to write zeros in the memory cell.