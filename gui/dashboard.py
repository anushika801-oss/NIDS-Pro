import customtkinter as ctk
from datetime import datetime
import queue
import time

from .styles import *
from .sidebar import Sidebar
from .traffic import TrafficTable
from .charts import ChartPanel
from .statistics import StatisticsPage
from .reports import ReportsPage
from .settings import SettingsPage
from .alerts import AlertPanel


class AlertPopup(ctk.CTkToplevel):
    def __init__(self, parent, title, message, severity="CRITICAL"):
        super().__init__(parent)

        self.title("⚠ THREAT ALERT")
        self.geometry("480x300")
        self.configure(fg_color=BACKGROUND)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.after(50, self._center_on_parent, parent)

        border_color = DANGER if severity == "CRITICAL" else WARNING

        outer = ctk.CTkFrame(self, fg_color=border_color, corner_radius=10)
        outer.pack(fill="both", expand=True, padx=6, pady=6)

        inner = ctk.CTkFrame(outer, fg_color=CARD, corner_radius=8)
        inner.pack(fill="both", expand=True, padx=2, pady=2)

        icon = "🔴" if severity == "CRITICAL" else "🟠"
        ctk.CTkLabel(
            inner, text=f"{icon}  {severity} ALERT",
            font=("Consolas", 20, "bold"),
            text_color=DANGER if severity == "CRITICAL" else WARNING
        ).pack(anchor="w", padx=20, pady=(18, 4))

        ctk.CTkLabel(
            inner, text=title,
            font=("Consolas", 13, "bold"),
            text_color=PRIMARY
        ).pack(anchor="w", padx=20, pady=(0, 6))

        msg_box = ctk.CTkTextbox(
            inner, height=80, fg_color=TABLE,
            border_width=1, border_color=CARD_BORDER,
            corner_radius=6, text_color=TEXT_LIGHT,
            font=("Consolas", 11)
        )
        msg_box.pack(fill="x", padx=20, pady=(0, 12))
        msg_box.insert("end", message)
        msg_box.configure(state="disabled")

        ctk.CTkButton(
            inner, text="DISMISS",
            font=("Consolas", 12, "bold"),
            fg_color=BTN_NORMAL, border_width=1,
            border_color=border_color, text_color=border_color,
            hover_color=CARD_HOVER, height=36,
            command=self.destroy
        ).pack(pady=(0, 14))

    def _center_on_parent(self, parent):
        pw, ph = parent.winfo_width(), parent.winfo_height()
        px, py = parent.winfo_x(), parent.winfo_y()
        w, h = self.winfo_width(), self.winfo_height()
        self.geometry(f"+{px + (pw - w) // 2}+{py + (ph - h) // 2}")


class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("🛡️ CYBER_SHIELD // Network Intrusion Detection System")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.configure(fg_color=BACKGROUND)

        # Counters shared across pages
        self.packet_count = 0
        self.alert_count = 0
        self.high_count = 0
        self.unique_ips = set()

        # Popup cooldown to avoid flooding (minimum 3s between popups)
        self._last_popup_time = 0

        # Sidebar Navigation
        self.sidebar = Sidebar(self, self.change_page)
        self.sidebar.pack(side="left", fill="y")

        # Main Container
        self.container = ctk.CTkFrame(self, fg_color=BACKGROUND, corner_radius=0)
        self.container.pack(side="right", fill="both", expand=True)

        # ============================================================
        # DASHBOARD PAGE — Live Traffic Focus
        # ============================================================
        self.dashboard_page = ctk.CTkFrame(self.container, fg_color=BACKGROUND, corner_radius=0)

        # ---------- Dashboard Header ----------
        header = ctk.CTkFrame(
            self.dashboard_page,
            fg_color=HEADER,
            corner_radius=CARD_RADIUS,
            border_width=1,
            border_color=CARD_BORDER,
            height=80
        )
        header.pack(fill="x", padx=18, pady=(15, 10))
        header.pack_propagate(False)

        left_h = ctk.CTkFrame(header, fg_color="transparent")
        left_h.pack(side="left", padx=18, fill="y")
        ctk.CTkLabel(
            left_h, text="⚡ LIVE CAPTURE CONSOLE",
            font=("Consolas", 20, "bold"), text_color=PRIMARY
        ).pack(anchor="w", pady=(10, 0))
        ctk.CTkLabel(
            left_h, text="REAL-TIME NETWORK PACKET FEED",
            font=("Consolas", 10, "bold"), text_color=TEXT_DIM
        ).pack(anchor="w")

        right_h = ctk.CTkFrame(header, fg_color="transparent")
        right_h.pack(side="right", padx=18, fill="y")

        self.time_label = ctk.CTkLabel(
            right_h, text="",
            font=("Consolas", 13, "bold"), text_color=PRIMARY
        )
        self.time_label.pack(anchor="e", pady=(10, 0))
        self.status_label = ctk.CTkLabel(
            right_h, text="[ SECURE / RUNNING ]",
            font=("Consolas", 11, "bold"), text_color=SUCCESS
        )
        self.status_label.pack(anchor="e")
        self.update_clock()

        # ---------- Dashboard Body (Left: Traffic Table | Right: Control + Graph) ----------
        body = ctk.CTkFrame(self.dashboard_page, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=18, pady=(0, 15))

        # Left: Full live traffic table
        self.traffic = TrafficTable(body)
        self.traffic.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Right: Monitor Control Panel + Live Graph
        right_panel = ctk.CTkFrame(body, fg_color="transparent", width=420)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)

        # Monitor Controller Card
        ctrl_card = ctk.CTkFrame(
            right_panel,
            fg_color=CARD,
            corner_radius=CARD_RADIUS,
            border_width=1,
            border_color=CARD_BORDER
        )
        ctrl_card.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            ctrl_card, text="🔌 MONITOR CONTROL",
            font=("Consolas", 14, "bold"), text_color=TEXT_LIGHT
        ).pack(anchor="w", padx=15, pady=(12, 6))

        # Interface selection
        from scapy.all import conf as scapy_conf
        import config
        import packet_capture
        self._config = config
        self._packet_capture = packet_capture

        try:
            self.iface_map = {"[ AUTO ] Default Route Interface": None}
            for iface in scapy_conf.ifaces.values():
                if iface.name:
                    disp = f"{iface.name}"
                    if iface.description:
                        disp += f" ({iface.description})"
                    if iface.ip:
                        disp += f" [{iface.ip}]"
                    self.iface_map[disp] = iface.name
            self.iface_options = list(self.iface_map.keys())
        except Exception:
            self.iface_options = ["[ AUTO ] Default Route Interface"]
            self.iface_map = {"[ AUTO ] Default Route Interface": None}

        self.iface_var = ctk.StringVar(value=self.iface_options[0])
        self.iface_dropdown = ctk.CTkOptionMenu(
            ctrl_card,
            values=self.iface_options,
            variable=self.iface_var,
            font=("Consolas", 10),
            dropdown_font=("Consolas", 10),
            fg_color=BTN_NORMAL,
            button_color=CARD_BORDER,
            button_hover_color=PRIMARY,
            dropdown_fg_color=SIDEBAR,
            dropdown_hover_color=CARD_HOVER,
            text_color=PRIMARY,
            height=34
        )
        self.iface_dropdown.pack(fill="x", padx=12, pady=(0, 8))

        # Start / Stop Buttons Row
        btn_row = ctk.CTkFrame(ctrl_card, fg_color="transparent")
        btn_row.pack(fill="x", padx=12, pady=(0, 12))

        self.start_btn = ctk.CTkButton(
            btn_row,
            text="▶  START",
            font=("Consolas", 12, "bold"),
            fg_color=BTN_NORMAL,
            border_width=1,
            border_color=SUCCESS,
            text_color=SUCCESS,
            hover_color=CARD_HOVER,
            height=36,
            command=self.start_capture
        )
        self.start_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.stop_btn = ctk.CTkButton(
            btn_row,
            text="⏹  STOP",
            font=("Consolas", 12, "bold"),
            fg_color=BTN_NORMAL,
            border_width=1,
            border_color=DANGER,
            text_color=DANGER,
            hover_color=CARD_HOVER,
            height=36,
            command=self.stop_capture
        )
        self.stop_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))

        # Capture Status & Stats mini-labels
        stats_frame = ctk.CTkFrame(ctrl_card, fg_color=TABLE, corner_radius=CARD_RADIUS - 2)
        stats_frame.pack(fill="x", padx=12, pady=(0, 12))

        self.cap_status_label = ctk.CTkLabel(
            stats_frame, text="[ STATUS: MONITORING ]",
            font=("Consolas", 11, "bold"), text_color=SUCCESS
        )
        self.cap_status_label.pack(anchor="w", padx=10, pady=(6, 2))

        self.pkt_stat = ctk.CTkLabel(
            stats_frame, text="PACKETS: 0   |   ALERTS: 0   |   HOSTS: 0",
            font=("Consolas", 10), text_color=TEXT_DIM
        )
        self.pkt_stat.pack(anchor="w", padx=10, pady=(0, 6))

        # Live Graph
        self.charts = ChartPanel(right_panel)
        self.charts.pack(fill="both", expand=True)

        # ---------- Alert Panel (breach log) ----------
        self.alert_panel = AlertPanel(self.dashboard_page)
        self.alert_panel.pack(fill="both", padx=18, pady=(0, 10), expand=False)

        # ============================================================
        # OTHER PAGES
        # ============================================================
        self.statistics_page = StatisticsPage(self.container)
        self.reports_page = ReportsPage(self.container)
        self.settings_page = SettingsPage(self.container)

        self.pages = {
            "dashboard": self.dashboard_page,
            "statistics": self.statistics_page,
            "reports": self.reports_page,
            "settings": self.settings_page,
        }

        self.change_page("dashboard")

        # Start poller — queue-based batch updates every 250ms
        self.after(250, self.periodic_update)

    # ================================================================

    def update_clock(self):
        self.time_label.configure(text=datetime.now().strftime("%d %b %Y // %H:%M:%S"))
        self.after(1000, self.update_clock)

    def change_page(self, page):
        if not hasattr(self, "pages"):
            return
        if page not in self.pages:
            page = "dashboard"
        for frame in self.pages.values():
            frame.pack_forget()
        self.pages[page].pack(fill="both", expand=True)

    def start_capture(self):
        """Apply selected interface and start sniffing."""
        selected_display = self.iface_var.get()
        selected_name = self.iface_map.get(selected_display)
        self._config.SELECTED_IFACE = selected_name
        self._packet_capture.start_capture_thread()
        self.cap_status_label.configure(
            text=f"[ STATUS: CAPTURING — {selected_name or 'AUTO'} ]",
            text_color=SUCCESS
        )
        self.status_label.configure(text="[ CAPTURING / LIVE ]", text_color=SUCCESS)

    def stop_capture(self):
        """Stop the sniffing thread."""
        self._packet_capture.stop_capture()
        self.cap_status_label.configure(
            text="[ STATUS: STOPPED / IDLE ]",
            text_color=DANGER
        )
        self.status_label.configure(text="[ STOPPED / IDLE ]", text_color=DANGER)

    def periodic_update(self):
        """Timer-based queue poller: drains packet queue in batches every 250ms."""
        new_packets = []
        new_alerts = []

        while True:
            try:
                features, alerts = self._packet_capture.packet_queue.get_nowait()
                new_packets.append(features)
                if alerts:
                    for alert in alerts:
                        new_alerts.append((features, alert))
            except queue.Empty:
                break

        if new_packets:
            self.packet_count += len(new_packets)
            for f in new_packets:
                src = f.get("src_ip")
                if src and src != "SYSTEM":
                    self.unique_ips.add(src)

            # Update traffic table (cap renders to latest 30 per tick)
            for f in new_packets[-30:]:
                has_alert = any(
                    f.get("src_ip") == af.get("src_ip") for af, _ in new_alerts
                )
                self.traffic.add_packet(f, has_alert)

            # Update statistics counters
            for f in new_packets:
                self.statistics_page.update_counters(f)
            self.statistics_page.refresh_chart()

            # Chart update
            self.charts.add_packets_count(len(new_packets))
        else:
            self.charts.add_packets_count(0)

        if new_alerts:
            for features, alert in new_alerts:
                self.alert_count += 1
                alert_upper = alert.upper()
                if "[HIGH]" in alert_upper or "CRITICAL" in alert_upper:
                    self.high_count += 1
                self.reports_page.add_report(features, alert)
                self.statistics_page.add_threat_event(features.get("src_ip", "?"), alert)

                severity = "CRITICAL" if "[HIGH]" in alert_upper or "CRITICAL" in alert_upper else "MEDIUM"
                self.alert_panel.add_alert(alert, severity)

                if severity == "CRITICAL":
                    now = time.time()
                    if now - self._last_popup_time >= 3:
                        self._last_popup_time = now
                        src = features.get("src_ip", "Unknown")
                        dst = features.get("dst_ip", "Unknown")
                        AlertPopup(
                            self,
                            title=f"{src}  →  {dst}",
                            message=alert,
                            severity=severity
                        )

        # Update mini-stats bar on dashboard
        self.pkt_stat.configure(
            text=f"PACKETS: {self.packet_count}   |   ALERTS: {self.alert_count}   |   HOSTS: {len(self.unique_ips)}"
        )

        self.after(250, self.periodic_update)