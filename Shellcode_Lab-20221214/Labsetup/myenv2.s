section .text
  global _start
    _start:
	BITS 32
	jmp short two
    one:
 	pop ebx
 	xor eax, eax		; eax = 0x00000000
 	mov [ebx+12], al	; Use 0 to terminate the string
    mov [ebx+17], al	; Use 0 to terminate the string
    mov [ebx+22], al	; Use 0 to terminate the string
    mov [ebx+23], al	; Use 0 to fill the gap of the 4 bytes cell of memory
 	mov [ebx+24], ebx	; argv[0] points "/usr/bin/env" 
 	mov [ebx+28], eax	; argv[1] = 0
 	lea ecx, [ebx+24]	; Get the address of argv[]
 	
    lea edx, [ebx+13]   ; Load "a=11" address in edx
    mov [ebx+32], edx   ; env[0] points to "a=11"
    lea edx, [ebx+18]   ; Load "b=22" address in edx
    mov [ebx+36], edx   ; env[1] points to "b=22"
    mov [ebx+40], eax   ; env[2] = 0
    lea edx, [ebx+32]   ; Get the address of env[]

 	mov al,  0x0b		; eax = 0x0000000b
 	int 0x80
     two:
 	call one
 	db '/usr/bin/env*a=11*b=22**AAAABBBBCCCCDDDDEEEE'