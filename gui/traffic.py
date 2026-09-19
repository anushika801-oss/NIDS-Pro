import customtkinter as ctk
from tkinter import ttk
from datetime import datetime
from .styles import *


class TrafficTable(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color=CARD,
            corner_radius=CARD_RADIUS,
            border_width=1,
            border_color=CARD_BORDER
        )

        # ================= HEADER =================

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.pack(fill="x", padx=15, pady=(12,4))

        ctk.CTkLabel(
            header,
            text="📡 NETWORK_TRAFFIC_FEED",
            font=("Consolas", 15, "bold"),
            text_color=PRIMARY
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text="[ BUFFER_SIZE: 300 ]",
            text_color=TEXT_DIM,
            font=("Consolas", 10, "bold")
        ).pack(side="right")

        # ================= SYSTEM THEMED TREEVIEW =================

        columns = (
            "Time",
            "Source",
            "Destination",
            "Protocol",
            "Port",
            "Status"
        )

        style = ttk.Style()
        style.theme_use("clam")

        # Apply dark tactical styling to the Tkinter Treeview widget
        style.configure(
            "Treeview",
            background=BACKGROUND,
            foreground=TEXT_LIGHT,
            fieldbackground=BACKGROUND,
            borderwidth=0,
            rowheight=30,
            font=("Consolas", 10)
        )

        style.configure(
            "Treeview.Heading",
            background=HEADER,
            foreground=PRIMARY,
            font=("Consolas", 11, "bold"),
            relief="flat"
        )

        style.map(
            "Treeview",
            background=[("selected", CARD_HOVER)],
            foreground=[("selected", "#FFFFFF")]
        )

        self.table = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=18
        )

        widths = [90, 160, 160, 90, 80, 110]

        for col, width in zip(columns, widths):
            self.table.heading(col, text=col.upper())
            self.table.column(
                col,
                width=width,
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        # Tactical Alert/Safe tagging with neon colors
        self.table.tag_configure(
            "safe",
            foreground=SUCCESS
        )

        self.table.tag_configure(
            "alert",
            foreground=DANGER
        )
        
        self.table.tag_configure(
            "sys_error",
            foreground=WARNING
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(15, 0),
            pady=12
        )

        scrollbar.pack(
            side="right",
            fill="y",
            padx=(0, 15),
            pady=12
        )

    # ===================================

    def add_packet(self, features, alert=False):
        # Format the protocol display
        proto_num = features.get("protocol", "-")
        proto_name = str(proto_num)
        if proto_num == 6:
            proto_name = "TCP"
        elif proto_num == 17:
            proto_name = "UDP"
        elif proto_num == 1:
            proto_name = "ICMP"
        elif proto_num == "SYS":
            proto_name = "SYSTEM"
            
        status = "[ ATTACK ]" if alert else "[ SECURE ]"
        tag = "alert" if alert else "safe"
        
        if proto_num == "SYS":
            status = "[ FAILED ]"
            tag = "sys_error"

        self.table.insert(
            "",
            "end",
            values=(
                datetime.now().strftime("%H:%M:%S"),
                features.get("src_ip", "-"),
                features.get("dst_ip", "-"),
                proto_name,
                features.get("dst_port", "-"),
                status
            ),
            tags=(tag,)
        )

        # Cap the table size
        if len(self.table.get_children()) > 300:
            self.table.delete(self.table.get_children()[0])

        self.table.yview_moveto(1)