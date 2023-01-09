void main(){
    char* shell = getenv("MYSHELL1");
    if (shell){
        printf("\tValue: %s\n", shell);
        printf("\tAddress: %x\n", (unsigned int)shell);
    }
    char* argv1 = getenv("MYSHELL2");
    if (argv1){
        printf("\tValue: %s\n", argv1);
        printf("\tAddress: %x\n", (unsigned int)argv1);
    }
}