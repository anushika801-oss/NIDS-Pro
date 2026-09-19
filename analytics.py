import sqlite3

def get_stats():
    conn = sqlite3.connect("nids.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM alerts")
    total_alerts = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM alerts WHERE severity='High'")
    high_alerts = cursor.fetchone()[0]

    cursor.execute("SELECT alert, COUNT(*) FROM alerts GROUP BY alert")
    alert_types = cursor.fetchall()

    conn.close()

    return {
        "total_packets": 0,
        "total_alerts": total_alerts,
        "high_alerts": high_alerts,
        "unique_ips": 0,
        "alert_types": alert_types
    }