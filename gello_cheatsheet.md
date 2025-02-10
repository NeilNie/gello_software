## Quickstart

Step 1: calibrate
`python3 scripts/gello_get_offset.py --start-joints 0 0 0 -1.57 0 1.57 0.753 --joint-signs 1 -1 1 -1 1 -1 1 --port /dev/ttyUSB0`
modify numbers in 
`gello/agents/gello_agent.py`

step 2: verify in sim
`python3 experiments/run_env.py --agent=gello --gello_port=/dev/ttyUSB0`
`python3 experiments/launch_nodes.py --robot sim_panda`

step 3: run on real robot
`python3 experiments/run_env.py --agent=gello --gello_port=/dev/ttyUSB0`
`python3 experiments/launch_nodes.py --robot panda`

## Additional notes
`python3 -m mujoco.viewer`

change gripper behavior in 
`gello/robots/panda.py`

joint states are recorded in
`gello/robots/dynamixel.py`
