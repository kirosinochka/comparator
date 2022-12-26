import hashlib
from typing import Dict
from pathlib import Path


BLOCK_SIZE = 65536


def hash_file(filepath: str) -> str:
    file_hash = hashlib.sha256()
    with open(filepath, 'rb') as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(BLOCK_SIZE)

    return file_hash.hexdigest()


def get_file_hash_dict_for_dir(dir: str) -> Dict[str, str]:
    p = list(map(str, filter(lambda a: a.is_file(), Path(dir).rglob("*"))))
    res = {}
    for file in p:
        res[hash_file(file)] = file
    return res


def main():
    svn = get_file_hash_dict_for_dir("svn")
    engine = get_file_hash_dict_for_dir("engine")
    res = []
    for k in svn.keys() | engine.keys():
        res += [(svn.get(k), engine.get(k))]

    with open("result.csv", "w") as f:
        for a, b in res:
            print(f"{a}: {b}")
            f.write(f"{a},{b}\n")


if __name__ == '__main__':
    main()
