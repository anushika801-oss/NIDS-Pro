import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict, deque
import numpy as np
from .styles import *


class StatisticsPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color=BACKGROUND)

        # Traffic counters
        self.total = 0
        self.tcp = 0
        self.udp = 0
        self.icmp = 0
        self.other = 0

        # Analytics data
        self.threat_events = []         # list of (src_ip, alert_str)
        self.attacker_counts = defaultdict(int)   # src_ip -> count
        self.attack_type_counts = defaultdict(int) # attack type -> count

        # Heatmap data: src_ip -> set of dst_ports
        self.heatmap_src_ips = deque(maxlen=10)   # last 10 unique src IPs seen
        self.heatmap_ports = deque(maxlen=20)     # last 20 unique dst ports seen
        self.heatmap_matrix = defaultdict(lambda: defaultdict(int))  # ip->port->count

        # ---- Page Header ----
        ctk.CTkLabel(
            self, text="📊 ANALYTICS INTELLIGENCE",
            font=("Consolas", 24, "bold"), text_color=PRIMARY
        ).pack(anchor="w", padx=20, pady=(18, 2))
        ctk.CTkLabel(
            self, text="Protocol distribution · Traffic heatmap · Attacker intelligence",
            font=("Consolas", 10, "bold"), text_color=TEXT_DIM
        ).pack(anchor="w", padx=20, pady=(0, 12))

        # ---- TOP ROW: Metric Cards ----
        cards_row = ctk.CTkFrame(self, fg_color="transparent")
        cards_row.pack(fill="x", padx=20, pady=(0, 10))
        cards_row.columnconfigure((0, 1, 2, 3), weight=1)

        self.card_labels = {}
        card_defs = [
            ("📦 TOTAL PKTS", PRIMARY),
            ("🔵 TCP", CYAN),
            ("🟢 UDP", SUCCESS),
            ("🔴 THREATS", DANGER),
        ]
        for i, (title, color) in enumerate(card_defs):
            card = ctk.CTkFrame(cards_row, fg_color=CARD, corner_radius=CARD_RADIUS,
                                border_width=1, border_color=CARD_BORDER, height=80)
            card.grid(row=0, column=i, padx=6, sticky="nsew")
            card.pack_propagate(False)
            ctk.CTkLabel(card, text=title, font=("Consolas", 11, "bold"),
                         text_color=TEXT_DIM).pack(anchor="w", padx=12, pady=(10, 0))
            val = ctk.CTkLabel(card, text="0", font=("Consolas", 24, "bold"), text_color=color)
            val.pack(anchor="w", padx=12)
            self.card_labels[title] = val

        # ---- BODY: 3 column layout ----
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        body.columnconfigure(0, weight=2)  # heatmap
        body.columnconfigure(1, weight=1)  # pie + top attackers
        body.columnconfigure(2, weight=1)  # top attacks
        body.rowconfigure(0, weight=1)

        # ============ LEFT: HEATMAP ============
        heatmap_card = ctk.CTkFrame(body, fg_color=CARD, corner_radius=CARD_RADIUS,
                                    border_width=1, border_color=CARD_BORDER)
        heatmap_card.grid(row=0, column=0, padx=(0, 8), sticky="nsew")

        ctk.CTkLabel(heatmap_card, text="🌡️ TRAFFIC HEATMAP",
                     font=("Consolas", 13, "bold"), text_color=TEXT_LIGHT
                     ).pack(anchor="w", padx=15, pady=(12, 2))
        ctk.CTkLabel(heatmap_card, text="Source IP vs Destination Port",
                     font=("Consolas", 9, "bold"), text_color=TEXT_DIM
                     ).pack(anchor="w", padx=15, pady=(0, 6))

        self.heatmap_fig = Figure(figsize=(5.5, 4.5), dpi=95, facecolor=CARD)
        self.heatmap_ax = self.heatmap_fig.add_subplot(111)
        self.heatmap_canvas = FigureCanvasTkAgg(self.heatmap_fig, heatmap_card)
        self.heatmap_canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self._draw_empty_heatmap()

        # ============ MIDDLE: Pie + Top Attackers ============
        mid_col = ctk.CTkFrame(body, fg_color="transparent")
        mid_col.grid(row=0, column=1, padx=(0, 8), sticky="nsew")

        # Protocol Pie
        pie_card = ctk.CTkFrame(mid_col, fg_color=CARD, corner_radius=CARD_RADIUS,
                                border_width=1, border_color=CARD_BORDER)
        pie_card.pack(fill="x", pady=(0, 8))
        ctk.CTkLabel(pie_card, text="PROTOCOL DIST",
                     font=("Consolas", 13, "bold"), text_color=TEXT_LIGHT
                     ).pack(anchor="w", padx=15, pady=(10, 4))

        self.pie_fig = Figure(figsize=(3.5, 2.8), dpi=95, facecolor=CARD)
        self.pie_ax = self.pie_fig.add_subplot(111)
        self.pie_canvas = FigureCanvasTkAgg(self.pie_fig, pie_card)
        self.pie_canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self._draw_empty_pie()

        # Top Attacker IPs
        attacker_card = ctk.CTkFrame(mid_col, fg_color=CARD, corner_radius=CARD_RADIUS,
                                     border_width=1, border_color=CARD_BORDER)
        attacker_card.pack(fill="both", expand=True)

        ctk.CTkLabel(attacker_card, text="🎯 TOP ATTACKER IPs",
                     font=("Consolas", 13, "bold"), text_color=DANGER
                     ).pack(anchor="w", padx=15, pady=(10, 6))

        self.attacker_box = ctk.CTkTextbox(
            attacker_card, fg_color=TABLE, corner_radius=CARD_RADIUS - 2,
            border_width=1, border_color=CARD_BORDER,
            font=("Consolas", 10), text_color=TEXT_LIGHT
        )
        self.attacker_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.attacker_box.insert("end", "[ WAITING FOR THREATS ]\n")
        self.attacker_box.configure(state="disabled")

        # ============ RIGHT: Top Attack Types ============
        attack_card = ctk.CTkFrame(body, fg_color=CARD, corner_radius=CARD_RADIUS,
                                   border_width=1, border_color=CARD_BORDER)
        attack_card.grid(row=0, column=2, sticky="nsew")

        ctk.CTkLabel(attack_card, text="⚡ TOP ATTACK TYPES",
                     font=("Consolas", 13, "bold"), text_color=WARNING
                     ).pack(anchor="w", padx=15, pady=(10, 6))

        self.attack_type_box = ctk.CTkTextbox(
            attack_card, fg_color=TABLE, corner_radius=CARD_RADIUS - 2,
            border_width=1, border_color=CARD_BORDER,
            font=("Consolas", 10), text_color=TEXT_LIGHT
        )
        self.attack_type_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.attack_type_box.insert("end", "[ NO ATTACKS DETECTED YET ]\n")
        self.attack_type_box.configure(state="disabled")

    # ======================================================
    # DATA UPDATERS (called every 250ms from dashboard poller)
    # ======================================================

    def update_counters(self, features):
        """Fast counter update without any redrawing."""
        self.total += 1
        proto = features.get("protocol")
        if proto == 6:
            self.tcp += 1
        elif proto == 17:
            self.udp += 1
        elif proto == 1:
            self.icmp += 1
        else:
            self.other += 1

        # Update heatmap data
        src = features.get("src_ip")
        port = features.get("dst_port")
        if src and port:
            if src not in self.heatmap_src_ips:
                self.heatmap_src_ips.append(src)
            if port not in self.heatmap_ports:
                self.heatmap_ports.append(port)
            self.heatmap_matrix[src][port] += 1

        # Update card label values live
        self.card_labels["📦 TOTAL PKTS"].configure(text=str(self.total))
        self.card_labels["🔵 TCP"].configure(text=str(self.tcp))
        self.card_labels["🟢 UDP"].configure(text=str(self.udp))

    def add_threat_event(self, src_ip, alert_str):
        """Register a detected threat for analytics."""
        self.threat_events.append((src_ip, alert_str))
        self.attacker_counts[src_ip] += 1

        # Parse attack category from alert tag
        a = alert_str.upper()
        if "PORT SCAN" in a:
            self.attack_type_counts["Port Scan"] += 1
        elif "DOS" in a or "FLOOD" in a:
            self.attack_type_counts["DoS Attack"] += 1
        elif "BRUTE FORCE" in a:
            self.attack_type_counts["Brute Force"] += 1
        else:
            self.attack_type_counts["Other Threat"] += 1

        threat_total = sum(self.attack_type_counts.values())
        self.card_labels["🔴 THREATS"].configure(text=str(threat_total))
        self._refresh_attacker_list()
        self._refresh_attack_types()

    # ======================================================
    # CHART REFRESH (bulk redraw, called once per poll tick)
    # ======================================================

    def refresh_chart(self):
        """Redraw pie chart and heatmap once per poll tick."""
        self._draw_pie()
        self._draw_heatmap()

    def _draw_empty_heatmap(self):
        self.heatmap_ax.clear()
        self.heatmap_ax.set_facecolor(TABLE)
        self.heatmap_fig.patch.set_facecolor(CARD)
        self.heatmap_ax.text(
            0.5, 0.5, "[ WAITING FOR TRAFFIC ]",
            transform=self.heatmap_ax.transAxes,
            ha="center", va="center",
            color=TEXT_DIM, fontsize=11, fontfamily="Consolas"
        )
        self.heatmap_ax.set_xticks([])
        self.heatmap_ax.set_yticks([])
        for spine in self.heatmap_ax.spines.values():
            spine.set_color(CARD_BORDER)
        self.heatmap_canvas.draw()

    def _draw_heatmap(self):
        if not self.heatmap_src_ips or not self.heatmap_ports:
            return

        ips = list(self.heatmap_src_ips)
        ports = sorted(list(self.heatmap_ports))

        # Build matrix
        matrix = np.zeros((len(ips), len(ports)))
        for i, ip in enumerate(ips):
            for j, port in enumerate(ports):
                matrix[i][j] = self.heatmap_matrix.get(ip, {}).get(port, 0)

        self.heatmap_ax.clear()
        self.heatmap_ax.set_facecolor(TABLE)
        self.heatmap_fig.patch.set_facecolor(CARD)

        im = self.heatmap_ax.imshow(
            matrix, aspect="auto",
            cmap="YlOrRd",
            interpolation="nearest"
        )

        # Format axes
        self.heatmap_ax.set_yticks(range(len(ips)))
        self.heatmap_ax.set_yticklabels(
            [ip[-12:] if len(ip) > 12 else ip for ip in ips],
            color=TEXT_DIM, fontsize=8, fontfamily="Consolas"
        )
        self.heatmap_ax.set_xticks(range(len(ports)))
        self.heatmap_ax.set_xticklabels(
            [str(p) for p in ports],
            rotation=45, ha="right",
            color=TEXT_DIM, fontsize=8, fontfamily="Consolas"
        )

        self.heatmap_ax.set_xlabel("Destination Port", color=TEXT_DIM, fontsize=9)
        self.heatmap_ax.set_ylabel("Source IP", color=TEXT_DIM, fontsize=9)
        self.heatmap_ax.set_title(
            "PACKET DENSITY MAP", color=TEXT_LIGHT,
            fontsize=10, fontfamily="Consolas", weight="bold"
        )

        for spine in self.heatmap_ax.spines.values():
            spine.set_color(CARD_BORDER)

        self.heatmap_fig.tight_layout()
        self.heatmap_canvas.draw()

    def _draw_empty_pie(self):
        self.pie_ax.clear()
        self.pie_ax.set_facecolor(CARD)
        self.pie_fig.patch.set_facecolor(CARD)
        self.pie_ax.pie(
            [1], labels=["WAITING..."],
            colors=[TEXT_FADE],
            textprops={"color": "white", "fontsize": 9, "fontfamily": "Consolas"}
        )
        self.pie_canvas.draw()

    def _draw_pie(self):
        values = [self.tcp, self.udp, self.icmp, self.other]
        labels = ["TCP", "UDP", "ICMP", "OTHER"]
        colors = [PRIMARY, SUCCESS, SECONDARY, WARNING]

        self.pie_ax.clear()
        self.pie_ax.set_facecolor(CARD)
        self.pie_fig.patch.set_facecolor(CARD)

        if sum(values) == 0:
            self.pie_ax.pie([1], labels=["WAITING..."], colors=[TEXT_FADE],
                            textprops={"color": "white", "fontsize": 9, "fontfamily": "Consolas"})
        else:
            active_vals = [(v, l, c) for v, l, c in zip(values, labels, colors) if v > 0]
            v, l, c = zip(*active_vals)
            self.pie_ax.pie(
                v, labels=l, autopct="%1.0f%%",
                startangle=90, colors=c,
                textprops={"color": "white", "fontsize": 9, "fontfamily": "Consolas", "weight": "bold"}
            )
        self.pie_canvas.draw()

    def _refresh_attacker_list(self):
        """Rebuild top attacker IP scoreboard."""
        self.attacker_box.configure(state="normal")
        self.attacker_box.delete("1.0", "end")

        sorted_attackers = sorted(self.attacker_counts.items(), key=lambda x: x[1], reverse=True)
        for rank, (ip, count) in enumerate(sorted_attackers[:10], 1):
            bar = "█" * min(count, 20)
            self.attacker_box.insert("end", f"#{rank:02d} {ip:<18} [{count:>4}] {bar}\n")

        self.attacker_box.configure(state="disabled")

    def _refresh_attack_types(self):
        """Rebuild top attack types list."""
        self.attack_type_box.configure(state="normal")
        self.attack_type_box.delete("1.0", "end")

        sorted_types = sorted(self.attack_type_counts.items(), key=lambda x: x[1], reverse=True)
        total = sum(self.attack_type_counts.values())
        for rank, (attack_type, count) in enumerate(sorted_types, 1):
            pct = (count / total * 100) if total else 0
            bar = "█" * min(int(pct / 5), 20)
            self.attack_type_box.insert("end", f"#{rank} {attack_type}\n    {count} hits | {pct:.1f}% {bar}\n\n")

        self.attack_type_box.configure(state="disabled")