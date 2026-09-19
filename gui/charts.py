import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
from .styles import *


class ChartPanel(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color=CARD,
            corner_radius=CARD_RADIUS,
            border_width=1,
            border_color=CARD_BORDER
        )

        # =========================
        # HEADER PANEL
        # =========================

        title = ctk.CTkLabel(
            self,
            text="📈 THROUGHOUT_BANDWIDTH",
            font=("Consolas", 15, "bold"),
            text_color=PRIMARY
        )
        title.pack(anchor="w", padx=15, pady=(12, 2))

        subtitle = ctk.CTkLabel(
            self,
            text="Real-Time Network Packets Per Second (PPS)",
            font=("Consolas", 10, "bold"),
            text_color=TEXT_DIM
        )
        subtitle.pack(anchor="w", padx=15)

        # =========================
        # HISTORY BUFFER
        # =========================

        self.history = deque(maxlen=40)
        for _ in range(40):
            self.history.append(0)

        # =========================
        # MATPLOTLIB COMPONENT
        # =========================

        self.figure = Figure(
            figsize=(5.2, 3.6),
            dpi=100,
            facecolor=CARD
        )

        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            self
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(5, 12)
        )

        self.refresh()

    # ======================================

    def refresh(self):

        self.ax.clear()

        # Premium Dark Tactical Style
        self.ax.set_facecolor(TABLE)
        self.figure.patch.set_facecolor(CARD)

        self.ax.grid(
            color=CARD_BORDER,
            alpha=0.4,
            linestyle="--"
        )

        # Hide excess border outlines
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["left"].set_color(CARD_BORDER)
        self.ax.spines["bottom"].set_color(CARD_BORDER)

        self.ax.tick_params(colors=TEXT_DIM, labelsize=9)

        # Plot line with bright Neon Cyan
        self.ax.plot(
            list(self.history),
            color=PRIMARY,
            linewidth=2.5
        )

        # Gradient shading below the curve
        self.ax.fill_between(
            range(len(self.history)),
            list(self.history),
            color=PRIMARY,
            alpha=0.15
        )

        # Styled title inside chart area
        self.ax.set_title(
            "TRAFFIC VOLATILITY (PPS)",
            color=TEXT_LIGHT,
            fontsize=10,
            weight="bold",
            fontname="Consolas"
        )

        self.canvas.draw()

    # ======================================

    def add_packets_count(self, count):
        """Append packets-per-second count to rolling history and redraw (run once per tick)."""
        # Multiplied by 4 because this poller runs every 250ms (4 ticks = 1 second)
        pps = count * 4
        self.history.append(pps)
        self.refresh()

    # ======================================

    def add_alert(self, alert):
        """Spike the chart slightly on breach trigger to simulate anomaly."""
        if self.history[-1] > 0:
            self.history[-1] += int(self.history[-1] * 0.25) + 10
        else:
            self.history[-1] += 15
        self.refresh()