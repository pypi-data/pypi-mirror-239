"""opentrons_shared_data.robot: Submodule for handling robot definition data."""
from pathlib import Path
from typing import cast
from typing_extensions import Final

import json

from .. import get_shared_data_root

from .dev_types import RobotDefinition, RobotType

DEFAULT_ROBOT_DEFINITION_VERSION: Final = 1


def load(
    robot_type: RobotType, version: int = DEFAULT_ROBOT_DEFINITION_VERSION
) -> RobotDefinition:
    """Load the definition for the specified robot id."""
    for fi in Path(
        get_shared_data_root() / "robot" / "definitions" / f"{version}"
    ).iterdir():
        defn = json.load(fi.open("r"))
        if defn["robotType"] == robot_type:
            return cast(RobotDefinition, defn)
    raise KeyError(robot_type)
