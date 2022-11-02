obj-m += info_all_hooks.o
all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean

ins:
	sudo dmesg -C
	sudo insmod info_all_hooks.ko

rm:
	sudo rmmod info_all_hooks

