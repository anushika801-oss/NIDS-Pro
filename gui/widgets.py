import customtkinter as ctk
from .styles import *


# ==========================================
# CYBER SECTION TITLE
# ==========================================

class SectionTitle(ctk.CTkLabel):

    def __init__(self, parent, text):

        super().__init__(
            parent,
            text=f"// {text.upper()}",
            font=("Consolas", 18, "bold"),
            text_color=PRIMARY
        )


# ==========================================
# CYBER STATUS BADGE
# ==========================================

class StatusBadge(ctk.CTkFrame):

    def __init__(self, parent, text="MONITORING", color=SUCCESS):

        super().__init__(
            parent,
            fg_color=HEADER,
            corner_radius=BUTTON_RADIUS,
            height=42,
            border_width=1,
            border_color=CARD_BORDER
        )

        self.pack_propagate(False)

        self.label = ctk.CTkLabel(
            self,
            text=f"[ STATUS: {text.upper()} ]",
            font=("Consolas", 13, "bold"),
            text_color=color
        )

        self.label.pack(expand=True)

    def set_status(self, text, color):

        self.label.configure(
            text=f"[ STATUS: {text.upper()} ]",
            text_color=color
        )


# ==========================================
# TECHNICAL GLOWING CARD
# ==========================================

class Card(ctk.CTkFrame):

    def __init__(self, parent, title, icon, color):

        super().__init__(
            parent,
            fg_color=CARD,
            corner_radius=CARD_RADIUS,
            width=250,
            height=115,
            border_width=1,
            border_color=CARD_BORDER
        )

        self.pack_propagate(False)
        self.color = color

        # ---------------- TOP PANEL ----------------

        top = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=15,
            pady=(12, 0)
        )

        # Tech style icon container (no round circle, sharp cornered tiny box)
        icon_bg = ctk.CTkFrame(
            top,
            width=38,
            height=38,
            corner_radius=4,
            fg_color=color
        )

        icon_bg.pack(side="left")

        icon_bg.pack_propagate(False)

        ctk.CTkLabel(
            icon_bg,
            text=icon,
            font=("Segoe UI Emoji", 18),
            text_color="black"
        ).pack(expand=True)

        ctk.CTkLabel(
            top,
            text=title.upper(),
            font=("Consolas", 12, "bold"),
            text_color=TEXT_DIM
        ).pack(side="left", padx=10)

        # ---------------- VALUE READOUT ----------------

        self.value = ctk.CTkLabel(
            self,
            text="0",
            font=("Consolas", 28, "bold"),
            text_color=color
        )

        self.value.pack(
            anchor="w",
            padx=18,
            pady=(4, 0)
        )

        # ---------------- STATUS / SUBTEXT ----------------

        self.status = ctk.CTkLabel(
            self,
            text="[ LIVE_MONITOR ]",
            font=("Consolas", 9, "bold"),
            text_color=SUCCESS
        )

        self.status.pack(
            anchor="w",
            padx=18,
            pady=(0, 6)
        )

    def update(self, value):
        self.value.configure(
            text=str(value)
        )
        
        # Flash border briefly on update to simulate technical activity
        self.configure(border_color=self.color)
        self.after(150, lambda: self.configure(border_color=CARD_BORDER))


# ==========================================
# CYBER PAGE CONTAINER FRAME
# ==========================================

class PageFrame(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color=BACKGROUND,
            corner_radius=0
        )