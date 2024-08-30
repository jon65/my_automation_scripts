
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

bash
Copy code
chmod +x check_mac_memory.sh
Run the Script:

In the terminal, execute the script by running:

bash
Copy code
./check_mac_memory.sh
Script Explanation
pages_to_gb Function: Converts the number of memory pages to gigabytes. The page size on macOS is 16KB (16384 bytes).

get_memory_stats Function: Uses vm_stat to gather memory statistics and then calculates total, used, and free memory in gigabytes.

check_cpu Function: Uses the top command to display CPU usage statistics.

Troubleshooting
Command Not Found: Ensure you are running the script on macOS with the required commands (vm_stat, top, bc) available.
Permissions: Ensure the script has execution permissions by running chmod +x check_mac_memory.sh.
