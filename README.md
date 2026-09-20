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