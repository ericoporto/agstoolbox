import os
import sys
from pathlib import Path

from agstoolbox.core.utils.version import tag_to_version, tag_to_family, family_to_major, \
    family_to_minor

if os.path.isdir(os.path.join(".", "src")) and os.path.isfile(os.path.join(".", "setup.py")):
    sys.path.append(os.path.realpath("src"))
    sys.path.append(os.path.realpath("src/agstoolbox"))

from agstoolbox.core.utils.file import get_gp_candidates_in_dir

cur_dir = Path(__file__).resolve().parent


def test_get_gp_candidates_in_dir():
    print(cur_dir.as_posix())
    candidates = get_gp_candidates_in_dir(cur_dir.as_posix(), 'Game.agf')
    assert len(candidates) == 4
    c0 = Path(os.path.relpath(candidates[0], cur_dir)).as_posix()
    c1 = Path(os.path.relpath(candidates[1], cur_dir)).as_posix()
    c2 = Path(os.path.relpath(candidates[2], cur_dir)).as_posix()
    c3 = Path(os.path.relpath(candidates[3], cur_dir)).as_posix()
    my_set = {c0, c1, c2, c3}
    assert len(my_set) == 4
    assert 'resources/fakedir2/Game.agf' in my_set
    assert 'resources/fakedir2/fakedirA/Game.agf' in my_set
    assert 'resources/fakedir3/fakedir3/CopyGame/Game.agf' in my_set
    assert 'resources/otherfakedir/MinGame/Game.agf' in my_set


def test_tag_to_version():
    assert tag_to_version("v.3.5.1.14") == "3.5.1.14"
    assert tag_to_version("v.3.  6.1.14") == "3.6.1.14"
    assert tag_to_version("v.4.0.0.14") == "4.0.0.14"
    assert tag_to_version("3.4.3.14") == "3.4.3.14"
    assert tag_to_version("version.3.3.1.14") == "3.3.1.14"
    assert tag_to_version("vivaldi.1") == "vivaldi.1"


def test_tag_to_family():
    assert tag_to_family("v.3.5.1.14") == "3.5"
    assert tag_to_family("v.3.6.1.14") == "3.6"
    assert tag_to_family("v.4.0.0.14") == "4.0"
    assert tag_to_family("3.4.3.14") == "3.4"
    assert tag_to_family("3.3.1.14") == "3.3"
    assert tag_to_family("vivaldi.1") == "vivaldi.1"


def test_family_to_major():
    assert family_to_major("3.4") == "3"
    assert family_to_major("3.7") == "3"
    assert family_to_major("4.4") == "4"
    assert family_to_major("73.4") == "73"
    assert family_to_major("experimental") == "experimental"


def test_family_to_minor():
    assert family_to_minor("3.4") == "4"
    assert family_to_minor("3.7") == "7"
    assert family_to_minor("4.2") == "2"
    assert family_to_minor("73.4") == "4"
    assert family_to_minor("experimental") == "experimental"
