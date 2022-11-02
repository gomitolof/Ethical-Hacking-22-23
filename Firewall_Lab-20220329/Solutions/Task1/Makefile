obj-m += block_telnet_and_ICMP.o
all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean

ins:
	sudo dmesg -C
	sudo insmod block_telnet_and_ICMP.ko

rm:
	sudo rmmod block_telnet_and_ICMP

