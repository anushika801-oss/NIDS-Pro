import customtkinter as ctk
from .styles import *


class Sidebar(ctk.CTkFrame):

    def __init__(self, parent, callback):
        super().__init__(parent, width=230, fg_color=SIDEBAR, corner_radius=0)
        self.pack_propagate(False)
        self.callback = callback
        self.buttons = {}

        # ---- Logo / Branding ----
        ctk.CTkLabel(
            self, text="📡",
            font=("Segoe UI Emoji", 36), text_color=PRIMARY
        ).pack(pady=(25, 0))
        ctk.CTkLabel(
            self, text="CYBER_SHIELD",
            font=("Consolas", 18, "bold"), text_color=PRIMARY
        ).pack(pady=(2, 0))
        ctk.CTkLabel(
            self, text="TACTICAL NIDS CONSOLE",
            font=("Consolas", 9, "bold"), text_color=TEXT_DIM
        ).pack(pady=(0, 8))

        # Divider line
        divider = ctk.CTkFrame(self, height=1, fg_color=CARD_BORDER)
        divider.pack(fill="x", padx=15, pady=(0, 15))

        # ---- Navigation Menus ----
        menus = [
            ("🏠  LIVE CAPTURE",   "dashboard"),
            ("📊  ANALYTICS",      "statistics"),
            ("📄  FILE REPORTS",   "reports"),
            ("⚙️   SYSTEM SETUP",   "settings"),
        ]

        for text, page in menus:
            btn = ctk.CTkButton(
                self, text=text, anchor="w",
                height=44, corner_radius=BUTTON_RADIUS,
                fg_color="transparent",
                hover_color=CARD_HOVER,
                text_color=TEXT_LIGHT,
                font=("Consolas", 12, "bold"),
                command=lambda p=page: self.select(p)
            )
            btn.pack(fill="x", padx=12, pady=3)
            self.buttons[page] = btn

        # ---- Version footer ----
        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.pack(side="bottom", fill="x", pady=15)

        ctk.CTkFrame(bottom, height=1, fg_color=CARD_BORDER).pack(fill="x", padx=15, pady=(0, 10))
        ctk.CTkLabel(
            bottom, text="SECURE_SHELL v4.0",
            font=("Consolas", 9, "bold"), text_color=TEXT_FADE
        ).pack()

    def select(self, page):
        for p, btn in self.buttons.items():
            if p == page:
                btn.configure(
                    fg_color=BTN_NORMAL,
                    text_color=PRIMARY,
                    border_width=1,
                    border_color=PRIMARY
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=TEXT_LIGHT,
                    border_width=0
                )
        if self.callback is not None:
            self.callback(page)