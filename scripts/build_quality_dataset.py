import random
import argparse
from fastwarc import ArchiveIterator, WarcRecordType
from cs336_data.filtering.extract_context import extract_content
from resiliparse.parse.encoding import detect_encoding
from cs336_data.filtering.language_identification import predict_language
from cs336_data.filtering.harmful_content import detect_toxic, detect_nsfw
from cs336_data.filtering.gopher_quality_filters import gopher_quality_filter

def is_english(text: str):
    if not text or not text.strip():
        return None

    label, score = predict_language(text)
    if label not in ("en", "__label__en") or score < 0.7:
        return None

    return text


def build_positive_examples(src: str, limit: int):
    positives = []

    with open(src, "rb") as f:
        for record in ArchiveIterator(f):
            if record.record_type != WarcRecordType.response:
                continue

            if record.http_headers.status_code != 200:
                continue
            html = record.reader.read()
            text = extract_content(html)
            # english
            if is_english(text) is None:
                continue
            # not harmful
            label, score = detect_nsfw(text)
            if label != "__label__non-nsfw" or score < 0.9:
                continue
            # not toxic
            label, score = detect_toxic(text)
            if label != "__label__non-toxic" or score < 0.9:
                continue
            # gopher_quality
            if not gopher_quality_filter(text):
                continue
            text = " ".join(text.split())
            positives.append("__label__high "+text)
            if len(positives) >= limit:
                break
    return positives

def build_negative_examples(src: str, limit: int):
    negatives = []

    count = 0
    with open(src, "rb") as f:
        for record in ArchiveIterator(f):
            if record.record_type != WarcRecordType.conversion:
                continue

            try:
                html = record.reader.read()
                text = html.decode(detect_encoding(html))
            except (UnicodeDecodeError, LookupError, TypeError):
                continue

            # english
            if is_english(text) is None:
                continue

            text = " ".join(text.split())
            negative = "__label__low " + text
            if len(negatives) < limit:
                negatives.append(negative)
            else:
                i = random.randint(0, count)
                if i < limit:
                    negatives[i] = negative

            count += 1

    return negatives

def write_file(train_path: str, val_path, positives, negatives, ratio=0.1):
    data = positives + negatives
    random.shuffle(data)

    val_size = int(len(data) * ratio)
    val_data = data[:val_size]
    train_data = data[val_size:]

    with open(train_path, "w", encoding="utf-8") as f:
        for item in train_data:
            f.write(item + "\n")

    with open(val_path, "w", encoding="utf-8") as f:
        for item in val_data:
            f.write(item + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--positive", type=str, required=False, default="local-shared-data/subsampled_positive_urls.warc.gz")
    parser.add_argument("--negative", type=str, required=False, default="local-shared-data/furu/cs336_data/wet_files/_EnglishWetFile/2f77453343bff7bb63a2/4a897e205146ccb404d6/data.warc.wet.gz")
    parser.add_argument("--limit", type=int, required=True)
    parser.add_argument("--train", type=str, required=False, default="local-shared-data/quality_train.txt")
    parser.add_argument("--val", type=str, required=False, default="local-shared-data/quality_val.txt")


    args = parser.parse_args()

    positives = build_positive_examples(args.positive, args.limit)
    negatives = build_negative_examples(args.negative, args.limit)
    print(f"positive: {len(positives)}")
    print(f"negative: {len(negatives)}")

    write_file(args.train, args.val, positives, negatives)