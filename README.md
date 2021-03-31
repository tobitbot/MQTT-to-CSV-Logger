# MQTT-to-CSV-Logger
Small tool to log MQTT traffic to CSV file

CSV-Log scheme:

| Date & Time | Topic | Message |

To ship this script use e.g. pyinstaller:
    pip install pyinstaller
    pyinstaller --onfile logger.py