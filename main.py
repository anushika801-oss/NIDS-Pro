from gui.dashboard import Dashboard
import packet_capture

if __name__ == "__main__":
    app = Dashboard()

    packet_capture.dashboard = app
    packet_capture.start_capture_thread()

    app.mainloop()