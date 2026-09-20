# NIDS Pro — Network Intrusion Detection System

NIDS Pro is a signature-based Network Intrusion Detection System developed in Python to monitor network traffic and identify potentially suspicious activities using rule-based detection.

The system captures network packets, extracts relevant network information, applies predefined detection rules, generates security alerts, stores alert information, and presents network activity through a monitoring dashboard.

---

## Overview

NIDS Pro focuses on network traffic monitoring and basic intrusion detection using predefined signatures and traffic patterns.

The system analyzes information such as:

- Source IP address
- Destination IP address
- Source and destination ports
- Network protocols
- Traffic patterns
- Suspicious port activity

When a predefined rule is triggered, NIDS Pro generates an alert and records the detected activity.

---

## Objectives

The main objectives of NIDS Pro are:

- Monitor network traffic in real time
- Analyze source and destination IP addresses
- Monitor network protocols and ports
- Detect potentially suspicious network activity
- Identify port scanning activity
- Generate security alerts
- Store alert information for analysis
- Provide a visual security monitoring dashboard
- Generate basic security reports

---

## Features

- Real-time network traffic monitoring
- Source IP and destination IP analysis
- Protocol and port monitoring
- Signature-based intrusion detection
- Rule-based suspicious activity detection
- Port scan detection
- High-volume traffic detection
- Security alerts
- Network traffic statistics
- Alert storage using SQLite
- Security monitoring dashboard
- Alert and report generation

---

## Technologies & Tools

- Python
- CustomTkinter
- Scapy
- Matplotlib
- NumPy
- SQLite
- Nmap
- Linux / Kali Linux
- Windows

---

## How NIDS Pro Works

The basic workflow of NIDS Pro is:

```text
Network Traffic
      ↓
Packet Capture
      ↓
Feature Extraction
      ↓
Detection Engine
      ↓
Rule-Based Analysis
      ↓
Suspicious Activity Detected
      ↓
Alert Generation
      ↓
Database / Logs
      ↓
Dashboard & Reports
```

The packet capture module collects network packets using Scapy. Relevant packet information is extracted and passed to the detection engine. The detection engine compares the traffic against predefined rules and thresholds. When suspicious activity is detected, an alert is generated and the information can be stored for further analysis.

---

## Detection Rules

NIDS Pro uses predefined rules and thresholds to identify potentially risky or suspicious traffic.

### Monitored Network Services

| Service | Port | Severity |
|---|---:|---|
| Telnet | 23 | High |
| FTP | 21 | Medium |
| SSH | 22 | Medium |
| HTTP | 80 | Low |
| HTTPS | 443 | Low |

### Traffic-Based Detection

The system also includes rule-based detection for:

- Port scanning activity
- High-volume traffic / DoS patterns
- Potentially risky network services

These rules are signature-based and do not use machine learning.

---

## Project Structure

```text
NIDS-Pro/
│
├── main.py
├── packet_capture.py
├── detection.py
├── feature_engine.py
├── alert.py
├── database.py
├── analytics.py
├── report.py
├── config.py
├── log_utils.py
├── diagnose.py
│
├── gui/
│   ├── dashboard.py
│   ├── alerts.py
│   ├── cards.py
│   ├── charts.py
│   ├── reports.py
│   ├── settings.py
│   ├── sidebar.py
│   ├── statistics.py
│   ├── traffic.py
│   ├── widgets.py
│   └── styles.py
│
├── nids-dashboard.png
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/anushika801-oss/NIDS-Pro.git
```

Move into the project directory:

```bash
cd NIDS-Pro
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

Install the required packages using:

```bash
pip install -r requirements.txt
```

The project dependencies are:

```text
scapy==2.7.0
customtkinter==6.0.0
matplotlib==3.11.0
numpy==2.4.6
```

---

## Running the Project

After installing the dependencies, run:

```bash
python main.py
```

The NIDS Pro monitoring dashboard will start.

---

## Testing the Detection System

NIDS Pro can be tested by generating network traffic on the system where the application is running.

For example:

```bash
ping 8.8.8.8
```

The captured traffic can then be displayed through the NIDS Pro dashboard.

For security testing, the predefined detection rules can be triggered through appropriate network traffic and lab-based testing.

---

## Dashboard

The NIDS Pro dashboard provides a visual interface for monitoring network activity and security alerts.

![NIDS Pro Dashboard](nids-dashboard.png)

The dashboard includes:

- Network traffic monitoring
- Traffic statistics
- Security alerts
- Reports
- System settings
- Visual charts

---

## Alert and Report Generation

When suspicious traffic is detected, NIDS Pro generates security alerts based on the configured detection rules.

The project also provides functionality for storing alert information and generating reports for further analysis.

---

## Database

NIDS Pro uses SQLite for local storage of alert-related information.

The database helps maintain detected security events so they can be accessed by the application's reporting and analysis components.

---

## Security Concepts Demonstrated

This project demonstrates practical concepts related to:

- Network Intrusion Detection
- Packet Capture
- Network Traffic Analysis
- TCP/IP Networking
- Ports and Protocols
- Signature-Based Detection
- Rule-Based Detection
- Port Scan Detection
- Security Alerting
- Log Management
- Basic Network Security Monitoring

---

## Limitations

- Detection is based on predefined signatures and rules.
- The system does not use machine learning for threat detection.
- Detection capability depends on the configured rules and thresholds.
- It is intended as an educational and project-level NIDS rather than a complete enterprise security monitoring solution.
- Network packet capture may require appropriate permissions depending on the operating system.

---

## Future Enhancements

Possible future improvements include:

- More comprehensive detection signatures
- Additional protocol analysis
- Improved alert classification
- Advanced traffic analytics
- More detailed reporting
- Email or external notification integration
- Enhanced dashboard visualizations
- Support for additional security monitoring features

---

## Author

**Anushika**

BCA Student | Cybersecurity | Networking | IT Security

GitHub:  
https://github.com/anushika801-oss

LinkedIn:  
https://linkedin.com/in/anushika0208

---

## Conclusion

NIDS Pro demonstrates the implementation of a signature-based Network Intrusion Detection System using Python. It combines packet capture, feature extraction, rule-based detection, alert generation, database storage, and dashboard visualization to provide a basic platform for monitoring network security events.