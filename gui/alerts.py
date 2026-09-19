import customtkinter as ctk
from datetime import datetime
from .widgets import StatusBadge
from .styles import *


class AlertPanel(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color=CARD,
            corner_radius=CARD_RADIUS,
            border_width=1,
            border_color=CARD_BORDER
        )

        # ===========================
        # HEADER PANEL
        # ===========================

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.pack(fill="x", padx=15, pady=(12, 4))

        ctk.CTkLabel(
            header,
            text="🚨 BREACH_LOG_STREAM",
            font=("Consolas", 15, "bold"),
            text_color=DANGER
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text="[ THREAT_ALERTS ]",
            text_color=TEXT_DIM,
            font=("Consolas", 10, "bold")
        ).pack(side="right")

        # ===========================
        # TACTICAL TEXT CONSOLE
        # ===========================

        self.box = ctk.CTkTextbox(
            self,
            height=250,
            fg_color=TABLE,
            border_width=1,
            border_color=CARD_BORDER,
            corner_radius=CARD_RADIUS,
            text_color=PRIMARY,
            font=("Consolas", 11)
        )

        self.box.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(4, 10)
        )

        self.box.insert(
            "end",
            ">>> SYSTEM_GUARD: ACTIVE_MONITOR_ONLINE\n"
        )
        self.box.configure(state="disabled")

        # ===========================
        # RUNTIME STATUS
        # ===========================

        ctk.CTkLabel(
            self,
            text="SYSTEM INTEGRITY RUNTIME STATUS:",
            font=("Consolas", 11, "bold"),
            text_color=TEXT_DIM
        ).pack(anchor="w", padx=15)

        self.status = StatusBadge(
            self,
            "MONITORING",
            SUCCESS
        )

        self.status.pack(
            fill="x",
            padx=12,
            pady=(4, 12)
        )

    # =====================================

    def add_alert(self, message, severity="HIGH"):

        now = datetime.now().strftime("%H:%M:%S")
        self.box.configure(state="normal")

        if severity.upper() == "HIGH":
            tag = "CRITICAL"
            color_prefix = "🔴"
            self.status.set_status("BREACH DETECTED", DANGER)
        elif severity.upper() == "MEDIUM":
            tag = "WARNING"
            color_prefix = "🟠"
            self.status.set_status("SUSPICIOUS ACTIVITY", WARNING)
        elif severity.upper() == "LOW":
            tag = "INFO"
            color_prefix = "🟡"
            self.status.set_status("ANOMALY RECORDED", WARNING)
        else:
            tag = "SAFE"
            color_prefix = "🟢"
            self.status.set_status("MONITORING", SUCCESS)

        # Append structured alert to console
        self.box.insert(
            "end",
            f"{color_prefix} [{now}] [{tag}] // {message}\n"
        )

        self.box.configure(state="disabled")
        self.box.see("end")

    # =====================================

    def clear(self):

        self.box.configure(state="normal")
        self.box.delete("1.0", "end")

        self.box.insert(
            "end",
            ">>> SYSTEM_GUARD: ACTIVE_MONITOR_ONLINE\n"
        )
        self.box.configure(state="disabled")

        self.status.set_status(
            "MONITORING",
            SUCCESS
        )