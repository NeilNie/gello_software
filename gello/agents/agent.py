from typing import Any, Dict, Protocol
from dataclasses import dataclass

import numpy as np


@dataclass
class BimanualObservation:
    robot_l: Dict[str, Any]
    robot_r: Dict[str, Any]


class Agent(Protocol):
    def act(self, obs: Dict[str, Any]) -> np.ndarray:
        """Returns an action given an observation.

        Args:
            obs: observation from the environment.

        Returns:
            action: action to take on the environment.
        """
        raise NotImplementedError


class DummyAgent(Agent):
    def __init__(self, num_dofs: int):
        self.num_dofs = num_dofs

    def act(self, obs: Dict[str, Any]) -> np.ndarray:
        return np.zeros(self.num_dofs)


class BimanualAgent(Agent):
    def __init__(self, agent_left: Agent, agent_right: Agent):
        self.agent_left = agent_left
        self.agent_right = agent_right

    def act(self, obs: BimanualObservation) -> np.ndarray:
        return np.concatenate(
            [self.agent_left.act(obs.robot_l), self.agent_right.act(obs.robot_r)]
        )
