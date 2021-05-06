# MQTT-to-CSV-Logger
Small tool to log MQTT traffic to CSV file

CSV-Log scheme:

| Date & Time | Topic | Message |

To ship this script use e.g. pyinstaller:
    pip install pyinstaller
    pyinstaller --onfile logger.py
# Use a tool like tmux to run as background process
$ tmux ls (Lists active sessions)
$ tmux new -s <name> (starts a new shell with the given name)
$ tmux attach-session -t <name>