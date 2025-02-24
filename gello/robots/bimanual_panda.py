import time
from typing import Dict

import numpy as np

from gello.robots.robot import BimanualRobot
from gello.robots.panda import PandaRobot

MAX_OPEN = 0.09


class BimanualPandaRobot(BimanualRobot):
    """A class representing a UR robot."""

    def __init__(self, robot_l: PandaRobot, robot_r: PandaRobot):
        super().__init__(robot_l, robot_r)

    def num_dofs(self) -> int:
        """Get the number of joints of the robot.

        Returns:
            int: The number of joints of the robot.
        """
        return super().num_dofs()

    def get_joint_state(self) -> np.ndarray:
        """Get the current state of the leader robot.

        Returns:
            T: The current state of the leader robot.
        """
        return super().get_joint_state()

    def command_joint_state(self, joint_state: np.ndarray) -> None:
        """Command the leader robot to a given state.

        Args:
            joint_state (np.ndarray): The state to command the leader robot to.
        """
        super().command_joint_state(joint_state)

    def get_observations(self) -> Dict[str, np.ndarray]:
        super().get_observations()


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
