"""
NIDS DIAGNOSTIC TOOL
====================
Run this script AS ADMINISTRATOR while performing attacks from Kali.
It will show you EXACTLY what Scapy sees — source IPs, packet counts, interfaces.

Usage:
    .venv\Scripts\python.exe diagnose.py
"""

import time
import sys
from collections import defaultdict

print("=" * 60)
print("  NIDS DIAGNOSTIC TOOL")
print("  Run as Administrator. Perform your attack now.")
print("=" * 60)

# --- 1. List all available interfaces ---
print("\n[STEP 1] Available Network Interfaces:")
try:
    from scapy.all import conf, get_if_list
    for iface in conf.ifaces.values():
        print(f"  NAME: {iface.name:<40} IP: {iface.ip or 'N/A':<18} DESC: {iface.description or ''}")
except Exception as e:
    print(f"  ERROR listing interfaces: {e}")

# --- 2. Sniff ALL interfaces for 20 seconds and report ---
print("\n[STEP 2] Sniffing ALL interfaces for 20 seconds...")
print("  >>> PERFORM YOUR HPING3 / NMAP ATTACK NOW <<<\n")

from scapy.all import sniff
from scapy.layers.inet import IP

ip_counter = defaultdict(int)
iface_counter = defaultdict(int)
total = 0
start = time.time()

def analyze(pkt):
    global total
    total += 1
    if pkt.haslayer(IP):
        ip_counter[pkt[IP].src] += 1
    sniff_iface = getattr(pkt, "sniffed_on", "unknown")
    iface_counter[sniff_iface] += 1

try:
    sniff(
        filter="ip",
        prn=analyze,
        store=False,
        timeout=20
    )
except Exception as e:
    print(f"  ERROR sniffing: {e}")
    print("  Make sure you are running as Administrator and Npcap is installed!")
    sys.exit(1)

elapsed = time.time() - start
print(f"\n[RESULT] Captured {total} packets in {elapsed:.1f} seconds")
print(f"         Avg rate: {total/elapsed:.0f} pps\n")

print("[RESULT] Packets by SOURCE IP (top 20):")
sorted_ips = sorted(ip_counter.items(), key=lambda x: x[1], reverse=True)
for ip, count in sorted_ips[:20]:
    bar = "█" * min(count // 10, 40)
    print(f"  {ip:<22} {count:>6} pkts  {bar}")

print(f"\n[RESULT] Packets by Interface captured on:")
for iface_name, count in sorted(iface_counter.items(), key=lambda x: x[1], reverse=True):
    print(f"  {iface_name:<45} {count:>6} pkts")

print("\n[DIAGNOSIS]")
kali_ips = [ip for ip in ip_counter if ip.startswith("192.168.") or ip.startswith("10.") or ip.startswith("172.")]
if kali_ips:
    print(f"  ✅ Found private-range source IPs (possible VM traffic): {kali_ips}")
else:
    print("  ❌ NO private-range IPs found from VM!")
    print("  ❌ Kali's attack packets are NOT reaching Scapy.")
    print("  SOLUTION: In VirtualBox, change Kali's network to:")
    print("    - Adapter 1: NAT (for internet)")
    print("    - Adapter 2: Host-Only (for NIDS testing)")
    print("  Then attack the Host-Only gateway IP (192.168.56.1)")

print("\n[DONE] Copy and share this output to debug further.")