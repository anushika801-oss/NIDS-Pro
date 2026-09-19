from scapy.layers.inet import IP, TCP, UDP, ICMP


def extract_features(packet):

    if not packet.haslayer(IP):
        return None

    ip = packet[IP]

    features = {
        "src_ip": ip.src,
        "dst_ip": ip.dst,
        "protocol": ip.proto,
        "packet_size": len(packet),

        "src_port": None,
        "dst_port": None,

        "syn": False,
        "ack": False,
        "fin": False,
        "rst": False,
        "psh": False,
        "urg": False,
    }

    # ---------------- TCP ----------------

    if packet.haslayer(TCP):

        tcp = packet[TCP]

        features["src_port"] = tcp.sport
        features["dst_port"] = tcp.dport

        flags = int(tcp.flags)

        features["syn"] = bool(flags & 0x02)
        features["ack"] = bool(flags & 0x10)
        features["fin"] = bool(flags & 0x01)
        features["rst"] = bool(flags & 0x04)
        features["psh"] = bool(flags & 0x08)
        features["urg"] = bool(flags & 0x20)

    # ---------------- UDP ----------------

    elif packet.haslayer(UDP):

        udp = packet[UDP]

        features["src_port"] = udp.sport
        features["dst_port"] = udp.dport

    # ---------------- ICMP ----------------

    elif packet.haslayer(ICMP):

        features["protocol"] = 1

    return features