from collections import Counter
import os
from pathlib import Path
from typing import Tuple, List, Callable
import cutie


def folder_chooser(
    folder: Path, path_filter: Callable[[Path], bool] = lambda _: True
) -> Path:
    assert folder.is_dir()
    choices: List[Tuple[Path, str]] = []
    for root, _, files in os.walk(folder):
        res = dict(Counter([Path(f).suffix for f in files]))
        desc = " , ".join([f"{k}: {v}" for k, v in res.items()])
        if path_filter(Path(root)):
            choices.append((Path(root), desc))
    index = cutie.select([f"{p} ({d})" for p, d in choices])
    return choices[index][0]


def folder_chooser_multiple(
    folder: Path, path_filter: Callable[[Path], bool] = lambda _: True
) -> List[Path]:
    assert folder.is_dir()
    choices: List[Tuple[Path, str]] = []
    for root, _, files in os.walk(folder):
        res = dict(Counter([Path(f).suffix for f in files]))
        desc = " , ".join([f"{k}: {v}" for k, v in res.items()])
        if path_filter(Path(root)):
            choices.append((Path(root), desc))
    indexes = cutie.select_multiple([f"{p} ({d})" for p, d in choices])
    return [choices[i][0] for i in indexes]


if __name__ == "__main__":
    print(folder_chooser(Path("/home/quy/sage")))