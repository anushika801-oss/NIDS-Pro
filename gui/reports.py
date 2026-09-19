import customtkinter as ctk
from datetime import datetime
from .styles import *
from report import generate_report, generate_pdf_report, generate_docx_report


class ReportsPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color=BACKGROUND)

        # ---- Title ----
        ctk.CTkLabel(
            self, text="📄 THREAT_REPORTS_MANAGER",
            font=("Consolas", 24, "bold"), text_color=PRIMARY
        ).pack(anchor="w", padx=20, pady=(18, 2))
        ctk.CTkLabel(
            self, text="Historical security alert log with multi-format export",
            font=("Consolas", 10, "bold"), text_color=TEXT_DIM
        ).pack(anchor="w", padx=20, pady=(0, 10))

        # ---- Reports Log Box ----
        self.box = ctk.CTkTextbox(
            self, fg_color=CARD,
            corner_radius=CARD_RADIUS,
            border_width=1, border_color=CARD_BORDER,
            text_color=TEXT_LIGHT,
            font=("Consolas", 11)
        )
        self.box.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        self.box.insert("end", "[ WAITING FOR THREAT REPORTS ] // NO INCIDENTS RECORDED YET...\n")
        self.box.configure(state="disabled")

        # ---- Actions Row ----
        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.pack(fill="x", padx=20, pady=(0, 18))

        # Clear button
        ctk.CTkButton(
            bottom, text="🗑️ CLEAR LOGS",
            font=("Consolas", 11, "bold"),
            fg_color=BTN_NORMAL, border_width=1, border_color=DANGER,
            text_color=DANGER, hover_color=CARD_HOVER,
            height=36, width=130,
            command=self.clear
        ).pack(side="left", padx=(0, 8))

        # Status label
        self.status_label = ctk.CTkLabel(
            bottom, text="",
            font=("Consolas", 10, "bold"), text_color=SUCCESS
        )
        self.status_label.pack(side="left", padx=(0, 10))

        # Export buttons (right side)
        ctk.CTkButton(
            bottom, text="💾 SAVE .TXT",
            font=("Consolas", 11, "bold"),
            fg_color=BTN_NORMAL, border_width=1, border_color=TEXT_DIM,
            text_color=TEXT_DIM, hover_color=CARD_HOVER,
            height=36, width=120,
            command=self.save_txt
        ).pack(side="right", padx=(8, 0))

        ctk.CTkButton(
            bottom, text="📄 EXPORT .DOCX",
            font=("Consolas", 11, "bold"),
            fg_color=BTN_NORMAL, border_width=1, border_color=SECONDARY,
            text_color=SECONDARY, hover_color=CARD_HOVER,
            height=36, width=150,
            command=self.save_docx
        ).pack(side="right", padx=(8, 0))

        ctk.CTkButton(
            bottom, text="📋 EXPORT .PDF",
            font=("Consolas", 11, "bold"),
            fg_color=BTN_NORMAL, border_width=1, border_color=PRIMARY,
            text_color=PRIMARY, hover_color=CARD_HOVER,
            height=36, width=140,
            command=self.save_pdf
        ).pack(side="right", padx=(8, 0))

    # ======================================================

    def add_report(self, features, alert):
        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.box.configure(state="normal")

        # Clear placeholder text on first real entry
        if "WAITING FOR THREAT REPORTS" in self.box.get("1.0", "end-1c"):
            self.box.delete("1.0", "end")

        # Determine severity color prefix
        alert_upper = alert.upper()
        if "[HIGH]" in alert_upper or "CRITICAL" in alert_upper:
            tag = "🔴"
        elif "[MEDIUM]" in alert_upper:
            tag = "🟠"
        else:
            tag = "🟡"

        self.box.insert(
            "end",
            f"{tag} ┌─── [ INCIDENT // {now} ] ───────────────────────────────\n"
            f"   │ SOURCE      : {features.get('src_ip', '-')} → DEST: {features.get('dst_ip', '-')}\n"
            f"   │ PROTOCOL    : {features.get('protocol', '-')}\n"
            f"   │ TARGET PORT : {features.get('dst_port', '-')}\n"
            f"   │ THREAT      : {alert}\n"
            f"   └────────────────────────────────────────────────────────\n\n"
        )
        self.box.configure(state="disabled")
        self.box.see("end")

    def clear(self):
        self.box.configure(state="normal")
        self.box.delete("1.0", "end")
        self.box.insert("end", "[ WAITING FOR THREAT REPORTS ] // NO INCIDENTS RECORDED YET...\n")
        self.box.configure(state="disabled")
        self._flash_status("[ LOGS CLEARED ]", PRIMARY)

    def save_txt(self):
        try:
            fname = generate_report()
            self._flash_status(f"[ TXT SAVED → {fname} ]", SUCCESS)
        except Exception as e:
            self._flash_status(f"[ ERROR: {e} ]", DANGER)

    def save_pdf(self):
        try:
            fname = generate_pdf_report("nids_report.pdf")
            self._flash_status(f"[ PDF EXPORTED → {fname} ]", SUCCESS)
        except Exception as e:
            self._flash_status(f"[ ERROR: {e} ]", DANGER)

    def save_docx(self):
        try:
            fname = generate_docx_report("nids_report.docx")
            self._flash_status(f"[ DOCX EXPORTED → {fname} ]", SUCCESS)
        except Exception as e:
            self._flash_status(f"[ ERROR: {e} ]", DANGER)

    def _flash_status(self, msg, color):
        self.status_label.configure(text=msg, text_color=color)
        self.after(4000, lambda: self.status_label.configure(text=""))