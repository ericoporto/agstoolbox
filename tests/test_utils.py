import os
from pathlib import Path

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
