import customtkinter as ctk
from .widgets import Card
from .styles import *


class CardPanel(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.columnconfigure((0, 1, 2, 3), weight=1)

        # ==========================================
        # PANEL METRICS (CYBER COLOR ACCENTED)
        # ==========================================

        self.packet = Card(
            self,
            "Network Packets",
            "📦",
            PRIMARY
        )

        self.alert = Card(
            self,
            "Detected Alerts",
            "🚨",
            DANGER
        )

        self.high = Card(
            self,
            "Critical Threats",
            "⚠️",
            WARNING
        )

        self.ip = Card(
            self,
            "Active Hosts",
            "🌐",
            SUCCESS
        )

        # ==========================================
        # METRIC GRID LAYOUT
        # ==========================================

        self.packet.grid(
            row=0,
            column=0,
            padx=6,
            pady=6,
            sticky="nsew"
        )

        self.alert.grid(
            row=0,
            column=1,
            padx=6,
            pady=6,
            sticky="nsew"
        )

        self.high.grid(
            row=0,
            column=2,
            padx=6,
            pady=6,
            sticky="nsew"
        )

        self.ip.grid(
            row=0,
            column=3,
            padx=6,
            pady=6,
            sticky="nsew"
        )

    # =============================================

    def update_packets(self, value):
        self.packet.update(value)

    def update_alerts(self, value):
        self.alert.update(value)

    def update_high(self, value):
        self.high.update(value)

    def update_ips(self, value):
        self.ip.update(value)