import customtkinter as ctk
import platform
import config
from .styles import *


class SettingsPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color=BACKGROUND)

        ctk.CTkLabel(
            self, text="⚙️ SYSTEM_SETTINGS",
            font=("Consolas", 24, "bold"), text_color=PRIMARY
        ).pack(anchor="w", padx=20, pady=(18, 2))
        ctk.CTkLabel(
            self, text="Detection engine threshold tuning and system specifications",
            font=("Consolas", 10, "bold"), text_color=TEXT_DIM
        ).pack(anchor="w", padx=20, pady=(0, 12))

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        container.columnconfigure(0, weight=1, uniform="col")
        container.columnconfigure(1, weight=1, uniform="col")

        # ===== LEFT: Threshold Sliders =====
        left_frame = ctk.CTkFrame(
            container, fg_color=CARD,
            corner_radius=CARD_RADIUS, border_width=1, border_color=CARD_BORDER
        )
        left_frame.grid(row=0, column=0, padx=(0, 10), sticky="nsew")

        ctk.CTkLabel(
            left_frame, text="⚔️ DETECTOR THRESHOLD TUNING",
            font=("Consolas", 13, "bold"), text_color=TEXT_LIGHT
        ).pack(anchor="w", padx=15, pady=(15, 10))

        self.create_slider(left_frame, "TIME WINDOW (SECONDS)", 1, 30,
                           config.TIME_WINDOW, self.update_time_window)
        self.create_slider(left_frame, "PORT SCAN THRESHOLD (UNIQUE PORTS)", 5, 100,
                           config.PORT_SCAN_THRESHOLD, self.update_port_scan)
        self.create_slider(left_frame, "DOS THRESHOLD (PACKETS/WINDOW)", 500, 10000,
                           config.DOS_THRESHOLD, self.update_dos)
        self.create_slider(left_frame, "BRUTE FORCE THRESHOLD (ATTEMPTS)", 3, 50,
                           config.BRUTE_FORCE_THRESHOLD, self.update_brute_force)

        # ===== RIGHT: System Info =====
        right_frame = ctk.CTkFrame(
            container, fg_color=CARD,
            corner_radius=CARD_RADIUS, border_width=1, border_color=CARD_BORDER
        )
        right_frame.grid(row=0, column=1, padx=(10, 0), sticky="nsew")

        ctk.CTkLabel(
            right_frame, text="💻 SYSTEM SPECIFICATIONS",
            font=("Consolas", 13, "bold"), text_color=TEXT_LIGHT
        ).pack(anchor="w", padx=15, pady=(15, 12))

        info = [
            ("APPLICATION", "CYBER_SHIELD NIDS"),
            ("VERSION", "4.0"),
            ("OS", platform.system()),
            ("OS RELEASE", platform.release()),
            ("ARCHITECTURE", platform.machine()),
            ("PYTHON", platform.python_version()),
            ("DETECTION", "Signature-Based IDS"),
            ("CAPTURE LIB", "Scapy + Npcap"),
        ]

        for name, value in info:
            row = ctk.CTkFrame(right_frame, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=5)
            ctk.CTkLabel(
                row, text=name, width=160, anchor="w",
                font=("Consolas", 11, "bold"), text_color=TEXT_DIM
            ).pack(side="left")
            ctk.CTkLabel(
                row, text=value, anchor="w",
                font=("Consolas", 11), text_color=PRIMARY
            ).pack(side="left")

        ctk.CTkLabel(
            right_frame,
            text="🛡️ SECURE // REAL-TIME NETWORK MONITORING ACTIVE",
            font=("Consolas", 11, "bold"), text_color=SUCCESS
        ).pack(anchor="w", padx=15, pady=(20, 15))

    # =========================================

    def create_slider(self, parent, label, min_val, max_val, default, update_fn):
        row_frame = ctk.CTkFrame(parent, fg_color="transparent")
        row_frame.pack(fill="x", padx=15, pady=10)

        top_info = ctk.CTkFrame(row_frame, fg_color="transparent")
        top_info.pack(fill="x")
        ctk.CTkLabel(
            top_info, text=label,
            font=("Consolas", 10, "bold"), text_color=TEXT_DIM
        ).pack(side="left")
        val_label = ctk.CTkLabel(
            top_info, text=str(default),
            font=("Consolas", 11, "bold"), text_color=PRIMARY
        )
        val_label.pack(side="right")

        slider = ctk.CTkSlider(
            row_frame, from_=min_val, to=max_val,
            number_of_steps=max_val - min_val,
            fg_color=CARD_BORDER, progress_color=PRIMARY,
            button_color=PRIMARY, button_hover_color=SECONDARY, height=16,
            command=lambda v, vl=val_label, fn=update_fn: self._on_slide(v, vl, fn)
        )
        slider.set(default)
        slider.pack(fill="x", pady=(4, 0))

    def _on_slide(self, value, val_label, update_fn):
        v = int(value)
        val_label.configure(text=str(v))
        update_fn(v)

    def update_time_window(self, val):
        config.TIME_WINDOW = val

    def update_port_scan(self, val):
        config.PORT_SCAN_THRESHOLD = val

    def update_dos(self, val):
        config.DOS_THRESHOLD = val

    def update_brute_force(self, val):
        config.BRUTE_FORCE_THRESHOLD = val