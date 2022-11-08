#include <stdio.h>
int main() {
	char *kernel_data_addr = (char*)0xcd63d16b;
	char kernel_data = *kernel_data_addr;
	printf("I have reached here.\n");
	return 0;
}
