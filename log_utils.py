import os
from datetime import datetime
import config


def log_alert(alert, severity="MEDIUM"):
    """Write alert to log file, creating parent directories if needed."""
    log_file = getattr(config, "LOG_FILE", r"data\alerts.log")
    
    # Auto-create parent directory
    parent_dir = os.path.dirname(log_file)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)
    
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"{time_str} | {severity} | {alert}\n")