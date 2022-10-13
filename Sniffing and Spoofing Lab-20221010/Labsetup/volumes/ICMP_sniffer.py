#!/usr/bin/env python3
from scapy.all import *
import subprocess

def print_pkt(pkt):
    pkt.show()

cmd = "ip address | grep 10.9.0.1 | awk '{print $7}'"
IFACE = subprocess.run(cmd, shell=True, check=True, universal_newlines=True, stdout=subprocess.PIPE).stdout.strip()
pkt = sniff(iface=IFACE, filter='icmp', prn=print_pkt)