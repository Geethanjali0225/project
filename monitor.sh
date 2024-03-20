#!/bin/bash

# Log file for CPU, RAM, and timestamp
log_file="performance_log.csv"

# Print column headers to the log file
echo "CPU %, %MEM, TIME+, COMMAND" > "$log_file"

# Main loop to monitor `top` and record data
while true; do
  top_output=$(top -b -n 1 | tail -n +8)

  while IFS= read -r line; do
    cpu_usage=$(echo "$line" | awk '{print $9}')
    mem_usage=$(echo "$line" | awk '{print $10}')
    timestamp=$(echo "$line" | awk '{print $11}')
    command=$(echo "$line" | awk '{$1=$2=$3=$4=$5=$6=$7=$8=$9=$10=$11=""; print $0}')

    # Remove leading and trailing spaces
    command=$(echo "$command" | xargs)

    echo "$cpu_usage, $mem_usage, $timestamp, $command" >> "$log_file"
  done <<< "$top_output"

  sleep 1
done
