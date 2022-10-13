#include <pcap.h>
#include <stdio.h>
#include <stdlib.h>

/* IP header */
struct sniff_ip {
	u_char ip_vhl;		/* version << 4 | header length >> 2 */
	u_char ip_tos;		/* type of service */
	u_short ip_len;		/* total length */
	u_short ip_id;		/* identification */
	u_short ip_off;		/* fragment offset field */
#define IP_RF 0x8000		/* reserved fragment flag */
#define IP_DF 0x4000		/* don't fragment flag */
#define IP_MF 0x2000		/* more fragments flag */
#define IP_OFFMASK 0x1fff	/* mask for fragmenting bits */
	u_char ip_ttl;		/* time to live */
	u_char ip_p;		/* protocol */
	u_short ip_sum;		/* checksum */
	struct in_addr ip_src,ip_dst; /* source and dest address */
};
#define IP_HL(ip)		(((ip)->ip_vhl) & 0x0f)
#define IP_V(ip)		(((ip)->ip_vhl) >> 4)

/* ethernet headers are always exactly 14 bytes */
#define SIZE_ETHERNET 14

/* This function will be invoked by pcap for each captured packet.
We can process each packet inside the function. */
void got_packet(u_char *args, const struct pcap_pkthdr *header, const u_char *packet) {
	const struct sniff_ip *ip; /* The IP header */
    printf("Got 1 packet\n");
    ip = (struct sniff_ip*)(packet + SIZE_ETHERNET);
    printf("\tsrc: %s\n", inet_ntoa(ip->ip_src));
    printf("\tdst: %s\n", inet_ntoa(ip->ip_dst));
}

int main() {
    pcap_t *handle;
    char errbuf[PCAP_ERRBUF_SIZE];
    struct bpf_program fp;
    char filter_exp[] = "icmp";
    bpf_u_int32 net;
    // Step 1: Open live pcap session on NIC with name eth3.
    // Students need to change "eth3" to the name found on their own
    // machines (using ifconfig). The interface to the 10.9.0.0/24
    // network has a prefix "br-" (if the container setup is used).
    /*
    pcap_open_live: generate the session, set the device to monitor and other options (e.g., promisc mode)
    */
    handle = pcap_open_live("br-0d592f2d7fdc", BUFSIZ, 1, 1000, errbuf);
    // Step 2: Compile filter_exp into BPF psuedo-code
    /*
    pcap_compile: if needed, compile a filter
    */
    pcap_compile(handle, &fp, filter_exp, 0, net);
    /*
    pcap_setfilter: set a previously compiled filter
    */
    if (pcap_setfilter(handle, &fp) !=0) {
        pcap_perror(handle, "Error:");
        exit(EXIT_FAILURE);
    }
    // Step 3: Capture packets
    /*
    pcap_loop: monitor the traffic and perform an action when receiving not filtered packets
    */
    pcap_loop(handle, -1, got_packet, NULL);
    pcap_close(handle);
    return 0;
    //Close the handle
}
// Note: don't forget to add "-lpcap" to the compilation command.
// For example: gcc -o sniff sniff.c -lpcap