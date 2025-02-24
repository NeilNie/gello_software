#!/usr/bin/env bash

# Name of the tmux session
SESSION_NAME="bimanual_sim"

# 1. Create a new tmux session (detached)
tmux new-session -d -s "$SESSION_NAME"

# Split the window into two panes side by side (horizontal split)
tmux split-window -h -t "$SESSION_NAME:0"

# 2. In both panes, run `conda activate vlm-policy` and then
# 3. `cd ../`
# 4. In the first pane, run the command with robot_port=6001
tmux send-keys -t "$SESSION_NAME:0.0" "conda activate vlm-policy" C-m
tmux send-keys -t "$SESSION_NAME:0.0" "cd ../" C-m
tmux send-keys -t "$SESSION_NAME:0.0" "python3 experiments/launch_nodes.py --robot sim_panda --robot_port 6001 --hostname 127.0.0.1" C-m

# 5. In the second pane, run the command with robot_port=6002
tmux send-keys -t "$SESSION_NAME:0.1" "conda activate vlm-policy" C-m
tmux send-keys -t "$SESSION_NAME:0.1" "cd ../" C-m
tmux send-keys -t "$SESSION_NAME:0.1" "python3 experiments/launch_nodes.py --robot sim_panda --robot_port 6001 --hostname 127.0.0.2" C-m

# Finally, attach to the session so it's visible in the terminal
tmux attach-session -t "$SESSION_NAME"
