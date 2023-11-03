import logging
import sys
from argparse import ArgumentParser
from functools import partial
from typing import NamedTuple

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(format="%(levelname)s - %(message)s")


class Coordinate(int):
    relative: bool

    def __new__(cls, value: int, relative=False):
        self = super().__new__(cls, value)
        self.relative = relative
        return self


class Location(NamedTuple):
    x: Coordinate
    y: Coordinate
    z: Coordinate


class Orientation(NamedTuple):
    x: bool
    y: bool
    z: bool


class UserError(Exception):
    pass


def get_args():
    parser = ArgumentParser(
        description="Generate music compositions in Minecraft noteblocks",
    )
    parser.add_argument("path_in", help="path to music source file/folder")
    parser.add_argument("path_out", help="path to Minecraft world")
    parser.add_argument(
        "--location",
        nargs="*",
        default=["~", "~", "~"],
        help="build location (in x y z); default is ~ ~ ~",
    )
    parser.add_argument(
        "--dimension",
        default=None,
        help="build dimension; default is player's dimension",
    )
    parser.add_argument(
        "--orientation",
        nargs="*",
        default=["+", "+", "+"],
        help=("build orientation (in x y z); default is + + +"),
    )
    parser.add_argument(
        "--theme",
        default="stone",
        help="opaque block for redstone components; default is stone",
    )
    parser.add_argument(
        "--blend",
        action="store_true",
        help=("blend the structure in with its environment (EXPERIMENTAL)"),
    )
    return parser.parse_args(None if sys.argv[1:] else ["-h"])


def parse_args():
    args = get_args()

    # location
    if len(args.location) != 3:
        raise UserError("3 coordinates are required")
    _location: list[Coordinate] = []
    for arg in args.location:
        if relative := arg.startswith("~"):
            arg = arg[1:]
        if not arg:
            value = 0
        else:
            try:
                value = int(arg)
            except ValueError:
                raise UserError(f"Expected integer coordinates; found {arg}")
        _location.append(Coordinate(value, relative=relative))
    location = Location(*_location)

    # dimension
    choices = ["overworld", "the_nether", "the_end"]
    if (dimension := args.dimension) is not None:
        if dimension not in choices:
            raise UserError(
                f"{dimension} is not a valid dimension; expected one of {choices}"
            )
        dimension = "minecraft:" + dimension

    # orientation
    if len(args.orientation) != 3:
        raise UserError("3 orientations are required")
    _orientation: list[bool] = []
    _options = "+-"
    for arg in args.orientation:
        try:
            _orientation.append(_options.index(arg) == 0)
        except ValueError:
            raise UserError(f"{arg} is not a valid direction; expected + or -")
    orientation = Orientation(*_orientation)

    # theme
    theme = args.theme

    # blend
    blend = args.blend

    # parse music
    from .parser import parse

    composition = parse(args.path_in)

    # load world
    from .generator import World

    world = World(args.path_out)
    return partial(
        world.generate,
        composition=composition,
        location=location,
        dimension=dimension,
        orientation=orientation,
        theme=theme,
        blend=blend,
    )


def main():
    try:
        generator = parse_args()
        generator()
    except UserError as e:
        logger.error(e)
        sys.exit(1)
    logger.info("All done!")


if __name__ == "__main__":
    main()
