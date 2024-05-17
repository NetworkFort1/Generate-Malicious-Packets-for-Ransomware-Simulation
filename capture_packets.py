from scapy.all import sniff, wrpcap, IP

def packet_callback(packet):
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        # Check if the packet is between the encoder and the server
        if (src_ip == '172.16.0.24' and dst_ip == '172.16.0.20') or (src_ip == '172.16.0.20' and dst_ip == '172.16.0.24'):
            print(f"Packet captured: {packet.summary()}")
            # Write the packet to a .cap file
            wrpcap('captured_packets.cap', packet, append=True)

# Sniff packets and call packet_callback for each packet
sniff(prn=packet_callback)