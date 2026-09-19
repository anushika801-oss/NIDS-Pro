import time
from collections import defaultdict
import config


class DetectionEngine:
    def __init__(self):
        # DoS trackers (target = victim IP)
        self.syn_tracker = defaultdict(list)
        self.udp_tracker = defaultdict(list)
        self.icmp_tracker = defaultdict(list)

        # Port scan tracker
        self.port_tracker = defaultdict(list)

        # Brute-force tracker
        self.bruteforce_tracker = defaultdict(list)

        # Alert cooldown tracker
        self.last_alert = {}

    def detect_threats(self, features):
        alerts = []

        if features is None:
            return alerts

        now = time.time()

        src = features.get("src_ip")
        dst = features.get("dst_ip")
        port = features.get("dst_port")
        proto = features.get("protocol")

        # Load thresholds dynamically
        time_window = config.TIME_WINDOW
        dos_threshold = config.DOS_THRESHOLD
        port_scan_threshold = config.PORT_SCAN_THRESHOLD
        brute_force_threshold = config.BRUTE_FORCE_THRESHOLD
        brute_force_ports = config.BRUTE_FORCE_PORTS
        cooldown = config.ALERT_COOLDOWN

        # =====================================================
        # TCP SYN FLOOD
        # =====================================================
        if dst and features.get("syn") and not features.get("ack"):

            self.syn_tracker[dst].append(now)

            self.syn_tracker[dst] = [
                t for t in self.syn_tracker[dst]
                if now - t <= time_window
            ]

            if len(self.syn_tracker[dst]) >= dos_threshold:

                if now - self.last_alert.get(("syn", dst), 0) > cooldown:

                    alerts.append(
                        f"CRITICAL | TCP SYN Flood targeting {dst} "
                        f"({len(self.syn_tracker[dst])} SYN packets)"
                    )

                    self.last_alert[("syn", dst)] = now

        # =====================================================
        # UDP FLOOD
        # =====================================================
        if dst and proto == 17:

            self.udp_tracker[dst].append(now)

            self.udp_tracker[dst] = [
                t for t in self.udp_tracker[dst]
                if now - t <= time_window
            ]

            if len(self.udp_tracker[dst]) >= dos_threshold:

                if now - self.last_alert.get(("udp", dst), 0) > cooldown:

                    alerts.append(
                        f"CRITICAL | UDP Flood targeting {dst} "
                        f"({len(self.udp_tracker[dst])} packets)"
                    )

                    self.last_alert[("udp", dst)] = now

        # =====================================================
        # ICMP FLOOD
        # =====================================================
        if dst and proto == 1:

            self.icmp_tracker[dst].append(now)

            self.icmp_tracker[dst] = [
                t for t in self.icmp_tracker[dst]
                if now - t <= time_window
            ]

            if len(self.icmp_tracker[dst]) >= dos_threshold:

                if now - self.last_alert.get(("icmp", dst), 0) > cooldown:

                    alerts.append(
                        f"CRITICAL | ICMP Flood targeting {dst} "
                        f"({len(self.icmp_tracker[dst])} packets)"
                    )

                    self.last_alert[("icmp", dst)] = now

        # =====================================================
        # PORT SCAN
        # =====================================================
        if src and dst and port is not None and features.get("syn"):

            key = (src, dst)

            self.port_tracker[key].append((port, now))

            self.port_tracker[key] = [
                (p, t)
                for p, t in self.port_tracker[key]
                if now - t <= time_window
            ]

            unique_ports = {p for p, t in self.port_tracker[key]}

            if len(unique_ports) >= port_scan_threshold:

                if now - self.last_alert.get(("scan", src), 0) > cooldown:

                    alerts.append(
                        f"HIGH | Port Scan detected from {src} "
                        f"({len(unique_ports)} unique ports)"
                    )

                    self.last_alert[("scan", src)] = now

        # =====================================================
        # BRUTE FORCE
        # =====================================================
        if (
            src
            and port in brute_force_ports
            and proto == 6
            and features.get("syn")
            and not features.get("ack")
        ):

            self.bruteforce_tracker[src].append(now)

            self.bruteforce_tracker[src] = [
                t for t in self.bruteforce_tracker[src]
                if now - t <= time_window
            ]

            if len(self.bruteforce_tracker[src]) >= brute_force_threshold:

                if now - self.last_alert.get(("brute", src), 0) > cooldown:

                    alerts.append(
                        f"MEDIUM | Brute Force attack from {src} "
                        f"on port {port}"
                    )

                    self.last_alert[("brute", src)] = now

        return alerts