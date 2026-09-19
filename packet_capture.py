import queue
import threading
from scapy.all import sniff
import config
from feature_engine import extract_features
from detection import DetectionEngine
from alert import show_alert

engine = DetectionEngine()

# Thread-safe queue for GUI updates
packet_queue = queue.Queue()
stop_sniffing = False
capture_thread = None


def process_packet(packet):
    features = extract_features(packet)
    if features is None:
        return

    alerts = engine.detect_threats(features)

    if alerts:
        show_alert(alerts)

    # Put features + alerts into the queue for the GUI periodic poller
    packet_queue.put((features, alerts))


def _sniff_worker(iface):
    """Worker function that runs Scapy sniff — blocks until stop_sniffing is set."""
    global stop_sniffing
    stop_sniffing = False

    try:
        if iface:
            # Sniff on a specific selected interface
            sniff(
                iface=iface,
                filter="ip",
                prn=process_packet,
                store=False,
                stop_filter=lambda p: stop_sniffing
            )
        else:
            # Sniff on ALL interfaces simultaneously (catches NAT + Wi-Fi + Loopback)
            # This is the correct mode for catching VirtualBox NAT traffic
            sniff(
                filter="ip",
                prn=process_packet,
                store=False,
                stop_filter=lambda p: stop_sniffing
            )
    except Exception as e:
        err_msg = f"Sniffer error (iface={iface or 'ALL'}): {e}. Run as Administrator + check Npcap."
        print(err_msg)
        packet_queue.put((
            {
                "src_ip": "SYSTEM", "dst_ip": "ERROR",
                "protocol": "SYS", "dst_port": "-", "packet_size": 0
            },
            [f"ERROR: {err_msg}"]
        ))


def start_capture_thread():
    """Start a fresh sniff thread. Stops any existing thread first."""
    global capture_thread, stop_sniffing

    # Signal any running thread to stop
    stop_sniffing = True

    # Drain leftover queue
    while not packet_queue.empty():
        try:
            packet_queue.get_nowait()
        except queue.Empty:
            break

    # Launch new sniffer thread on the configured interface
    iface = getattr(config, "SELECTED_IFACE", None)
    capture_thread = threading.Thread(
        target=_sniff_worker,
        args=(iface,),
        daemon=True
    )
    capture_thread.start()


def stop_capture():
    """Signal the sniffer thread to stop."""
    global stop_sniffing
    stop_sniffing = True