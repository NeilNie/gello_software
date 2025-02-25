from typing import Dict
import numpy as np
from gello.agents.dynamixel_robot_config import DynamixelRobotConfig


# default USB0 is right
# default USB1 is left


PORT_CONFIG_MAP: Dict[str, DynamixelRobotConfig] = {
    "/dev/ttyGelloRight": DynamixelRobotConfig(
        joint_ids=(1, 2, 3, 4, 5, 6, 7),
        joint_offsets=(
            6*np.pi/4, 4*np.pi/4, 8*np.pi/4, 4*np.pi/4, 4*np.pi/4, 4*np.pi/4, 5*np.pi/4
        ),
        joint_signs=(1, 1, 1, -1, 1, -1, 1),
        gripper_config=(8, 2.5 * 180 / np.pi, 3.5 * 180 / np.pi),
    ),
    "/dev/ttyGelloLeft": DynamixelRobotConfig(
        joint_ids=(1, 2, 3, 4, 5, 6, 7),
        joint_offsets=(
            2*np.pi/4, 4*np.pi/4, 2*np.pi/4, 10*np.pi/4, 6*np.pi/4, 2*np.pi/4, -1*np.pi/4
        ),
        joint_signs=(1, -1, 1, 1, 1, 1, 1),
        gripper_config=(8, 2.5 * 180 / np.pi, 3.5 * 180 / np.pi),
    ),
}
