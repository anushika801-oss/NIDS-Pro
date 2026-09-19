from datetime import datetime
from log_utils import log_alert
from database import save_alert


def parse_severity(alert):
    """Extract severity tag from the threat string like [HIGH], [LOW], [MEDIUM]."""
    alert_upper = alert.upper()
    if "[HIGH]" in alert_upper or "CRITICAL" in alert_upper:
        return "High"
    elif "[MEDIUM]" in alert_upper:
        return "Medium"
    elif "[LOW]" in alert_upper:
        return "Low"
    return "Medium"


def show_alert(alerts):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for alert in alerts:
        severity = parse_severity(alert)
        log = f"{current_time} | {alert} | {severity}"
        print("\n========== ALERT ==========")
        print(log)
        log_alert(alert, severity)
        save_alert(alert, severity)