
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

## Installation

1. **Download the Script**:

   Save the following script as `check_mac_memory.sh`:

   ```bash
   #!/bin/bash

   # Function to convert pages to GB
   pages_to_gb() {
       local pages=$1
       local page_size=16384 # in bytes (16KB)
       echo "scale=2; $pages * $page_size / 1024 / 1024 / 1024" | bc
   }

   # Function to get memory statistics
   get_memory_stats() {
       echo "Checking RAM utilization on macOS..."
       
       # Get the output of vm_stat
       vm_stats=$(vm_stat)
       
       # Extract the values
       pages_free=$(echo "$vm_stats" | awk '/Pages free/ {print $3}' | sed 's/\.//')
       pages_active=$(echo "$vm_stats" | awk '/Pages active/ {print $3}' | sed 's/\.//')
       pages_inactive=$(echo "$vm_stats" | awk '/Pages inactive/ {print $3}' | sed 's/\.//')
       pages_wired_down=$(echo "$vm_stats" | awk '/Pages wired down/ {print $4}' | sed 's/\.//')
       
       # Calculate total RAM in pages
       total_pages=$((pages_free + pages_active + pages_inactive + pages_wired_down))
       
       # Convert values to GB
       total_ram_gb=$(pages_to_gb "$total_pages")
       used_ram_gb=$(pages_to_gb "$((pages_active + pages_inactive + pages_wired_down))")
       free_ram_gb=$(pages_to_gb "$pages_free")
       
       echo "Total RAM: $total_ram_gb GB"
       echo "Used RAM: $used_ram_gb GB"
       echo "Free RAM: $free_ram_gb GB"
   }

   # Function to check CPU utilization
   check_cpu() {
       echo "Checking CPU utilization on macOS..."
       top -l 1 -s 0 | grep "CPU usage" | awk '{print "CPU usage: " $3 " user, " $5 " sys, " $7 " idle"}'
   }

   # Main script execution
   echo "System Resource Utilization"
   echo "--------------------------"
   get_memory_stats
   echo
   check_cpu
