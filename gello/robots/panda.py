import time
from typing import Dict

import numpy as np
from deoxys import config_root
from deoxys.franka_interface import FrankaInterface
from deoxys.utils import YamlConfig

from gello.robots.robot import Robot

MAX_OPEN = 0.09


class PandaRobot(Robot):
    """A class representing a UR robot."""

    def __init__(self, robot_ip: str = "100.97.47.74"):

        self.robot = FrankaInterface(
            config_root + "/charmander.yml",
            use_visualizer=False
        )
        self.gripper = None

        self._controller_cfg = YamlConfig(config_root + "/joint-impedance-controller.yml").as_easydict()
        time.sleep(1)

    def num_dofs(self) -> int:
        """Get the number of joints of the robot.

        Returns:
            int: The number of joints of the robot.
        """
        return 8

    def get_joint_state(self) -> np.ndarray:
        """Get the current state of the leader robot.

        Returns:
            T: The current state of the leader robot.
        """
        last_q = np.array(self.robot.last_q)
        gripper_width = np.array(self.robot.last_gripper_q)
        pos = np.append(last_q, gripper_width / MAX_OPEN)
        return pos

    def command_joint_state(self, joint_state: np.ndarray) -> None:
        """Command the leader robot to a given state.

        Args:
            joint_state (np.ndarray): The state to command the leader robot to.
        """
        joint_action, gripper_action = joint_state[:-1], joint_state[-1]

        joint_upper_limit = np.array([
            2.9671,
            1.8326,
            2.9671,
            0,
            2.9671,
            3.8223,
            2.9671
        ])
        joint_lower_limit = np.array([
            -2.9671,
            -1.8326,
            -2.9671,
            -3.1416,
            -2.9671,
            -0.0873,
            -2.9671
        ])

        assert np.all(joint_upper_limit >= joint_action) and np.all(joint_lower_limit <= joint_action), "Joint limits violated"

        old_gripper_action = gripper_action
        gripper_action = -1 if gripper_action >= 0.8 else 1
        # print(f"gripper action: {old_gripper_action}, {gripper_action}")

        # for joint in joint_traj:
        action = joint_action.tolist() + [gripper_action]
        self.robot.control(
            controller_type="JOINT_IMPEDANCE",
            action=action,
            controller_cfg=self._controller_cfg,
        )

    def get_observations(self) -> Dict[str, np.ndarray]:
        joints = self.get_joint_state()
        pos_quat = np.zeros(7)
        gripper_pos = np.array([joints[-1]])

        # gello original
        obs = {
            "joint_positions": joints,
            "joint_velocities": joints,
            "ee_pos_quat": pos_quat,
            "gripper_position": gripper_pos,
        }

        # what we addionally need
        prop = self._get_prop()
        obs.update(prop)

        return obs

    def _get_prop(self):
        prop = {}
        if len(self.robot._state_buffer) == 0:
            prop["q"] = []
            prop["eef_pos"] = []
            prop["eef_quat"] = []
            prop["tau_ext_hat_filtered"] = []
            prop["O_F_ext_hat_K"] = []
            prop["K_F_ext_hat_K"] = []

        else:
            robot_state = self.robot._state_buffer[-1]
            prop["q"] = list(np.array(robot_state.q))
            eef_quat, eef_pos = self.robot.last_eef_quat_and_pos
            prop["eef_pos"] = list(eef_pos[:, 0])
            prop["eef_quat"] = list(eef_quat)
            prop["O_T_EE"] = list(np.array(robot_state.O_T_EE))

            # force readings
            prop["tau_ext_hat_filtered"] = list(np.array(robot_state.tau_ext_hat_filtered))
            prop["O_F_ext_hat_K"] = list(np.array(robot_state.O_F_ext_hat_K))
            prop["K_F_ext_hat_K"] = list(np.array(robot_state.K_F_ext_hat_K))

        if len(self.robot._gripper_state_buffer) == 0:
            prop["gripper_width"] = None
        else:
            gripper_state = self.robot._gripper_state_buffer[-1]
            prop["gripper_width"] = np.array([gripper_state.width])
        prop["timestamp"] = time.time()
        return prop


def main():
    robot = PandaRobot()
    current_joints = robot.get_joint_state()
    # move a small delta 0.1 rad
    move_joints = current_joints + 0.05
    # make last joint (gripper) closed
    move_joints[-1] = 0.5
    time.sleep(1)
    m = 0.09
    robot.command_joint_state(move_joints)


if __name__ == "__main__":
    main()
