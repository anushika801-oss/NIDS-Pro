# ==========================================
# NIDS Dynamic Configuration Parameters
# ==========================================

# Port Scan — unique destination ports within TIME_WINDOW triggers alert
PORT_SCAN_THRESHOLD = 15

# DoS Attack — total packets TO the victim host within TIME_WINDOW
# NOTE: Scapy on Windows captures ~20-30% of actual flood traffic.
# hping3 --flood sends ~10k pps; Scapy sees ~1000-2000 pps.
# Set to 500 to reliably catch floods while avoiding false positives.
DOS_THRESHOLD = 500

# Rolling Time Window (seconds)
TIME_WINDOW = 10

# Brute Force Parameters — connection attempts to auth ports
BRUTE_FORCE_THRESHOLD = 15
BRUTE_FORCE_PORTS = [22, 21, 3389, 3306]

# Alert Cooldown (seconds between repeated alerts for same source)
ALERT_COOLDOWN = 10

# Log File Path
LOG_FILE = r"data\alerts.log"

# Default Sniffer Interface (None = Scapy default route interface)
SELECTED_IFACE = None