#!/usr/bin/env python3
from scapy.all import *

ip = IP()
ip.src = '1.2.3.4'
ip.dst = '10.9.0.5'
icmp = ip/ICMP()
icmp.type = "echo-request"
icmp.seq = 1
icmp.show()
send(icmp)