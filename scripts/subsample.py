import gzip
import random

src = "local-shared-data/wiki/enwiki-20260501-extracted_urls.txt.gz"
dst = "local-shared-data/subsampled_positive_urls.txt"

n = 10000
random.seed(42)

sample = []
count = 0

with gzip.open(src, "rt", encoding="utf-8") as f:
    for line in f:
        url = line.strip()

        if not url:
           continue

        if len(sample) < n:
           sample.append(url)
        else:
            j = random.randint(0, count)
            if j < n:
                sample[j] = url
        count += 1

with open(dst, "w", encoding="utf-8") as f:
    for url in sample:
        f.write(url + '\n')

print(f"save {n} samples to {dst}")


