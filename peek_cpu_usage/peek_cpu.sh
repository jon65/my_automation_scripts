#!/bin/bash

# Function to check RAM utilization and total memory on Linux
check_ram_linux() {
    echo "Checking RAM utilization on Linux..."
    total_ram=$(grep MemTotal /proc/meminfo | awk '{print $2}')
    used_ram=$(grep Active: /proc/meminfo | awk '{print $2}')
    free_ram=$(grep MemFree /proc/meminfo | awk '{print $2}')
    
    # Convert from kB to GB
    total_ram_gb=$(echo "scale=2; $total_ram / 1024 / 1024" | bc)
    used_ram_gb=$(echo "scale=2; $used_ram / 1024 / 1024" | bc)
    free_ram_gb=$(echo "scale=2; $free_ram / 1024 / 1024" | bc)
    
    echo "Total RAM: $total_ram_gb GB"
    echo "Used RAM: $used_ram_gb GB"
    echo "Free RAM: $free_ram_gb GB"
    
    # Summary
    echo "RAM Stats: Your system has $total_ram_gb GB of memory, with some pages actively used and others available."
}

# Function to check RAM utilization and total memory on macOS
check_ram_macos() {
    echo "Checking RAM utilization on macOS..."
    total_ram=$(system_profiler SPHardwareDataType | grep "Memory:" | awk '{print $2}')
    
    # Use vm_stat to get memory usage stats
    vm_stats=$(vm_stat)
    pages_free=$(echo "$vm_stats" | grep "Pages free:" | awk '{print $3}' | sed 's/.$//')
    pages_active=$(echo "$vm_stats" | grep "Pages active:" | awk '{print $3}' | sed 's/.$//')
    pages_wired=$(echo "$vm_stats" | grep "Pages wired down:" | awk '{print $4}' | sed 's/.$//')

    # Convert pages to GB (using a page size of 16KB)
    page_size_kb=16
    total_ram_gb=$(echo "scale=2; ($pages_active + $pages_free + $pages_wired) * $page_size_kb / 1024 / 1024" | bc)
    used_ram_gb=$(echo "scale=2; ($pages_active + $pages_wired) * $page_size_kb / 1024 / 1024" | bc)

    echo "Total RAM: $total_ram GB"
    echo "Used RAM: $used_ram_gb GB"
    echo "Free RAM: $(echo "scale=2; $total_ram_gb - $used_ram_gb" | bc) GB"
    
    # Summary
    echo "RAM Stats: Your system has $total_ram GB of memory, with some pages actively used and others available."
}

# Function to check CPU utilization
check_cpu() {
    echo "Checking CPU utilization..."
    if command -v top >/dev/null 2>&1; then
        if [ "$(uname)" == "Darwin" ]; then
            # For macOS
            cpu_usage=$(top -l 1 -s 0 | grep "CPU usage")
            echo "$cpu_usage"
        else
            # For Linux
            cpu_usage=$(top -bn1 | grep "Cpu(s)")
            echo "$cpu_usage"
        fi
    else
        echo "Unsupported OS for CPU check."
        exit 1
    fi
}

# Main script execution
echo "System Resource Utilization"
echo "--------------------------"

if command -v free >/dev/null 2>&1; then
    check_ram_linux
elif command -v system_profiler >/dev/null 2>&1; then
    check_ram_macos
else
    echo "Unsupported OS for RAM check."
    exit 1
fi

echo
check_cpu
