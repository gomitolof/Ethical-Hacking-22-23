#!/usr/bin/env python3
from scapy.all import *

def print_pkt(pkt):
    pkt.show()

pkt = sniff(iface='br-cc6114b3713d', filter='icmp', prn=print_pkt)