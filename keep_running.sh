#!/bin/bash
while true; do
    python3 your_script.py
    if [ -f done.flag ]; then
        echo "Job complete."
        break
    fi
    echo "Restarting..."
done
