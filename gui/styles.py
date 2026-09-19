import customtkinter as ctk

# =====================================
# WINDOW CONFIG
# =====================================

WINDOW_WIDTH = 1650
WINDOW_HEIGHT = 920

# =====================================
# CYBER THEME COLOR SYSTEM (OBSIDIAN & NEON)
# =====================================

# Obsidian Dark Backgrounds
BACKGROUND = "#04060A"       # Pure obsidian deep dark
SIDEBAR = "#080B12"          # Dark tactical slate
CARD = "#0C101B"             # Sleek panel background
CARD_HOVER = "#141B2E"       # Hover panel glow state
CARD_BORDER = "#1E293B"      # Standard cyber structural border
HEADER = "#080D18"           # Header element backdrop
TABLE = "#060A12"            # Dark grid data view

# Glowing Cyber Accents
PRIMARY = "#00F0FF"          # Cyber Neon Cyan
SECONDARY = "#BD00FF"        # Tactical Neon Purple
CYAN = "#00D8FF"
SUCCESS = "#00FF66"          # Tactical Green (Online / Clean)
WARNING = "#FF9F0A"          # Warning Gold
DANGER = "#FF0055"           # Breach Crimson (Critical Alert)
PINK = "#FF00AA"

# Text Colors
TEXT = "#FFFFFF"             # Crisp pure white
TEXT_LIGHT = "#E2E8F0"       # Light grey text
TEXT_DIM = "#94A3B8"         # Medium grey info text
TEXT_FADE = "#475569"        # Dark grey muted/placeholder

# Context-Specific Card Colors
PACKET_COLOR = "#00F0FF"      # Cyan for network bytes
ALERT_COLOR = "#FF0055"       # Crimson for triggered breaches
HIGH_COLOR = "#FF9F0A"        # Amber for warning level
IP_COLOR = "#00FF66"          # Green for active node mapping

# Interactive Button styling
BTN_NORMAL = "#101626"
BTN_HOVER = "#00F0FF"
BTN_ACTIVE = "#BD00FF"
BTN_TEXT = "#FFFFFF"

# Table Specifics
TABLE_HEADER = "#0F1626"
TABLE_ROW1 = "#080C14"
TABLE_ROW2 = "#0C111D"

# Graph Aesthetics
PIE_BLUE = "#00F0FF"
PIE_PURPLE = "#BD00FF"
PIE_GREEN = "#00FF66"
PIE_RED = "#FF0055"
PIE_ORANGE = "#FF9F0A"
PIE_CYAN = "#00E5FF"

# Operational Status Badges
ONLINE = "#00FF66"
OFFLINE = "#FF0055"
LIVE = "#00FF66"

# =====================================
# FONTS (CYBER MONOSPACE & SANS)
# =====================================

TITLE_FONT = ("Consolas", 28, "bold")
SUBTITLE_FONT = ("Segoe UI", 13)
CARD_TITLE = ("Consolas", 12, "bold")
CARD_VALUE = ("Consolas", 32, "bold")
HEADING = ("Consolas", 18, "bold")
NORMAL = ("Segoe UI", 12)
SMALL = ("Segoe UI", 11)
TINY = ("Segoe UI", 10)
MONO_SMALL = ("Consolas", 11)
MONO_NORMAL = ("Consolas", 12)

# =====================================
# CYBERNETIC GEOMETRY
# =====================================

CARD_RADIUS = 8              # Cyber looks use sharper, technical corners rather than bubbly ones
BUTTON_RADIUS = 6
TABLE_RADIUS = 6

# =====================================
# CUSTOMTKINTER CORE INITIALIZATION
# =====================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")