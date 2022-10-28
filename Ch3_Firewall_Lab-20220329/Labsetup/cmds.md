$ sudo insmod hello.ko # inserting a module
$ lsmod | grep hello # list modules
$ sudo rmmod hello # remove the module
$ dmesg # check the messages
$ modinfo hello.ko # to show information about a Linux Kernel module

// List all the rules in a table (without line number)
iptables -t nat -L -n
// List all the rules in a table (with line number)
iptables -t filter -L -n --line-numbers
// Delete rule No. 2 in the INPUT chain of the filter table
iptables -t filter -D INPUT 2
// Drop all the incoming packets that satisfy the <rule>
iptables -t filter -A INPUT <rule> -j DROP

iptables -F
iptables -P OUTPUT ACCEPT
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT