section .text
  global _start
    _start:
        ; Store the argument string on stack
        xor  eax, eax 
        push eax          ; Use 0 to terminate the string
        push "/env"
        push "/bin"
        push "/usr"
        mov  ebx, esp     ; Get the string address

        ; Construct the argument array argv[]
        push eax          ; argv[1] = 0
        push ebx          ; argv[0] points "/bin//sh"
        mov  ecx, esp     ; Get the address of argv[]
    
        ; For environment variable
        push eax
        mov edx, "4###"
        shl edx, 24
        shr edx, 24
        push edx
        push "=123"
        push "cccc"
        mov  edx, esp

        push eax
        push "5678"
        push "bbb="
        mov  esi, esp

        push eax
        push "1234"
        push "aaa="
        mov  edi, esp

        ; Construct the environment argument array env[]
        push eax
        push edx
        push esi
        push edi
        mov  edx, esp     ; Get the address of env[]

        ; Invoke execve()
        xor  eax, eax     ; eax = 0x00000000
        mov   al, 0x0b    ; eax = 0x0000000b
        int 0x80
