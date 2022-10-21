#!/usr/bin/env python3
from scapy.all import *
from random import randint
import subprocess

def spoof_reply(pkt):
    pkt.show()
    ttl=64
    id=randint(200, 60000)
    if pkt.getlayer(IP).dst[0:6] != "10.9.0.":
        ttl = 109
        id=0
    send(IP(src=pkt.getlayer(IP).dst, dst=pkt.getlayer(IP).src, ttl=ttl, id=id)/ICMP(type=0, id=pkt.getlayer(ICMP).id, seq=pkt.getlayer(ICMP).seq)/pkt.getlayer(Raw).load)

cmd = "ip a | grep 10.9.0.1 | awk '{print $7}'"
IFACE = subprocess.run(cmd, shell=True, check=True, universal_newlines=True, stdout=subprocess.PIPE).stdout.strip()
pkt = sniff(iface=IFACE, filter='icmp[icmptype] = icmp-echo', prn=spoof_reply)