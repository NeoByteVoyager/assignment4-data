import os
import random
import hashlib
import unicodedata
import regex as re
from pathlib import Path
from collections import defaultdict
from cs336_data.utils.union_find import UnionFind

def normalize_text(text: str) -> str:
    text = text.lower()

    text = unicodedata.normalize("NFD", text)
    text = "".join(
        c if unicodedata.category(c) != "Mn" else ""
        for c in text
    )

    text = "".join(
        " " if unicodedata.category(c).startswith("P") else c
        for c in text
    )
    text = re.sub(r"\s+", " ", text).strip()

    return text

def n_gram(text: str, n_gram_length) -> set[tuple[str, ...]]:
    words = text.split()
    n_gram = set(
        tuple(words[i: i + n_gram_length])
        for i in range(len(words) - n_gram_length + 1)
    )
    return n_gram

def stable_hash(gram: tuple[str, ...], seed: int) -> int:
    data = " ".join(gram).encode("utf-8")
    seed_bytes = seed.to_bytes(8, byteorder="big", signed=False)

    digest = hashlib.sha256(seed_bytes + data).digest()
    return int.from_bytes(digest, byteorder="big")

def get_minihashes(
    n_gram_set: set[tuple[str, ...]],
    seeds: list[int]
):
    minihashes = []
    for seed in seeds:
        minihash = None
        for gram in n_gram_set:
            hash_val = stable_hash(gram, seed)
            if minihash is None or hash_val < minihash:
                minihash = hash_val
        minihashes.append(minihash)
    return minihashes

def get_candidate_pairs(
    minihashes: list[list],
    hash_num: int,
    band_num: int,
):
    band_size = hash_num // band_num
    candidate_pairs = set()
    buckets = defaultdict(list)
    id = 0
    for minihash in minihashes:
        for i in range(0, hash_num, band_size):
            band_val = tuple(minihash[i: i + band_size])
            band_id = i // band_size
            candidates = buckets[(band_id, band_val)]
            for candidate in candidates:
                candidate_pairs.add((candidate, id))
            buckets[(band_id, band_val)].append(id)
        id += 1
    return candidate_pairs

def is_similar(
    text1: str,
    text2: str,
    n_gram_length: int,
    threshold: float
) -> bool:
    n_gram_set1 = n_gram(text1, n_gram_length)
    n_gram_set2 = n_gram(text2, n_gram_length)
    if len(n_gram_set2) == 0 and len(n_gram_set2) == 0:
        return text2 == text1
    else:
        return len(n_gram_set1 & n_gram_set2) / len(n_gram_set1 | n_gram_set2) > threshold

def minihash_deduplication(
    src: list[os.PathLike],
    hash_num: int,
    band_num: int,
    n_gram_length: int,
    similar_threshold: float,
    output_dir: os.PathLike
):
    '''
    output: the deduplication of the src to output_dir
    '''

    seeds = list(range(hash_num))
    # 1.compute minihash of the src
    minihashes = []
    texts = []
    for src_path in src:
        with open(src_path, "r", encoding="utf-8") as f:
            original_text = f.read()
        # normalize
        text = normalize_text(original_text)
        texts.append(text)
        # cut to n_gram
        n_gram_set = n_gram(text, n_gram_length)
        # calculate minihash
        minihashes.append(get_minihashes(n_gram_set, seeds))
    #print(minihashes)
    # 2. use LSH to select candient
    candidate_pairs = get_candidate_pairs(minihashes, hash_num, band_num)
    #print(candidate_pairs)
    # 3. verify the candidate_pairs and merge
    union_find = UnionFind(len(texts))
    for id1, id2 in candidate_pairs:
        if is_similar(texts[id1], texts[id2], n_gram_length, similar_threshold):
            union_find.union(id1, id2)

    save_ids = union_find.find_roots()

    # 4.save to output_dir
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for i in save_ids:
        src_path = src[i]

        file_name = Path(src_path).name
        new_path = output_dir / file_name

        with open(src_path, 'r', encoding="utf-8") as fin, \
            open(new_path, "w", encoding="utf-8") as fout:
            for line in fin:
                fout.write(line)


if __name__ == "__main__":
    path1 = "tests/fixtures/documents_with_fuzzy_duplicates/pytorch_license.txt"
    path2 = "tests/fixtures/documents_with_fuzzy_duplicates/rails_mit_license.txt"
    path3 = "tests/fixtures/documents_with_fuzzy_duplicates/react_mit_license.txt"
    minihash_deduplication([path1, path2, path3], 64, 16, 4, "outputs")

