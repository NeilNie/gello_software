#!/bin/bash

# Check if an argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 [left|right]"
    exit 1
fi

# Determine the port based on the argument
if [ "$1" = "left" ]; then
    PORT="/dev/ttyGelloLeft"
    JOINT_SIGNS="1 -1 1 1 1 1 1"
elif [ "$1" = "right" ]; then
    PORT="/dev/ttyGelloRight"
    JOINT_SIGNS="1 -1 1 -1 1 -1 1"
else
    PORT="$1"
    JOINT_SIGNS="1 -1 1 -1 1 -1 1"
fi

# Run the Python script with the selected port
python3 gello_get_offset.py \
    --start-joints 0 0 0 -1.57 0 1.57 0.753 \
    --joint-signs $JOINT_SIGNS \
    --port "$PORT"
