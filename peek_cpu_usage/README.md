
# System Resource Utilization Script
lightweight CLI alternative to activity Manager. 

I use this to quickly view my resource activity without needing to open a activity monitor app

This script checks the current RAM and CPU utilization on macOS, providing information similar to what is displayed in the Activity Monitor.

## Features

- **RAM Utilization**: Displays total RAM, used RAM, and free RAM in gigabytes.
- **CPU Utilization**: Displays current CPU usage percentages for user, system, and idle time.

## Requirements

- **macOS**: The script is specifically designed for macOS.
- **bash**: The script uses bash for execution.
- **bc**: Basic calculator for floating-point arithmetic.
Make the Script Executable:

Open a terminal and run:

nano peek_cpu.sh
copy code to file and save
chmod +x peek_cpu.sh
Run the Script:
./peek_cpu.sh

Alternatively, add the script to your global environment 
