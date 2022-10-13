#!/usr/bin/env python3
from scapy.all import *

assert len(sys.argv) == 2, "Usage: python3 traceroute.py <ip address>"
ip = IP()
addr = sys.argv[1]
assert isinstance(addr, str), "The IP address must be a string"
addr = ip.dst = str(addr)
icmp = ip/ICMP()
reachable = False

for ttl in range(1,30):
    icmp.ttl = ttl
    ans, unans = sr(icmp, retry = 3, timeout = 1, verbose = False)
    #ans.summary()
    if len(ans) == 0:
        print("%d) * * *" % (ttl))
    else:
        if ans[0][1].type == 3:
            break
        if ans[0][1].type == 11:
            print("%d) %s" % (ttl, ans[0][1].src))
        if ans[0][1].type == 0:
            reachable = True
            print(ttl, ") Destination", ans[0][1].src, "reached")
            break

if reachable == False:
    print("Destination unreachable")