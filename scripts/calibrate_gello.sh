#!/usr/bin/env bash

# Check if an argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <integer>"
    exit 1
fi

# Validate that the argument is an integer (non-negative)
if ! [[ "$1" =~ ^[0-9]+$ ]]; then
    echo "Error: argument must be an integer."
    exit 1
fi

# Execute the Python script with the provided integer

conda activate "vlm-policy"

python3 gello_get_offset.py \
    --start-joints 0 0 0 -1.57 0 1.57 0.753 \
    --joint-signs 1 -1 1 -1 1 -1 1 \
    --port "/dev/ttyUSB$1"
