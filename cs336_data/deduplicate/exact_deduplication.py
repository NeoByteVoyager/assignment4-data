import os
import hashlib
from pathlib import Path
from collections import defaultdict

def exact_line_deduplication(
        src: list[os.PathLike],
        dst: os.PathLike
):

    lines = defaultdict(int)
    for raw_path in src:
        with open(raw_path, "r", encoding="utf-8") as f:
            for line in f:
                h = hashlib.md5(line.encode("utf-8")).digest()
                lines[h] += 1

    for raw_path in src:
        filename = Path(raw_path).name
        new_path = dst / filename

        with open(raw_path, "r", encoding="utf-8") as fin,\
                open(new_path, "w", encoding="utf-8") as fout:
            for line in fin:
                h = hashlib.md5(line.encode("utf-8")).digest()
                if lines[h] == 1:
                    fout.write(line)








