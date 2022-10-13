#!/usr/bin/env python3
from scapy.all import *

ip = IP()
addr = input('Inserisci indirizzo IP: ')
ip.dst = addr
icmp = ip/ICMP()
reachable = False

for ttl in range(1,60):
    icmp.ttl = ttl
    ans, unans = sr(icmp, iface="eth0", loop=1, inter=0.2)
    if ans == None:
        print(ttl, ") * * *")
    else:
        print(ttl, ")", ans.src)
        if addr == ans.src:
            reachable = True
            break

if reachable == False:
    print("Destination unreachable")