import os
import argparse
from pathlib import Path
from fastwarc import ArchiveIterator,WarcRecordType
from resiliparse.parse.encoding import detect_encoding
from cs336_data.filtering.quality_classifier import predict_quality
from cs336_data.filtering.harmful_content import detect_toxic, detect_nsfw
from cs336_data.filtering.gopher_quality_filters import gopher_quality_filter
from cs336_data.filtering.mask_pii import mask_ip, mask_phone, mask_email
from cs336_data.deduplicate.minihash_deduplication import minihash_deduplication

def filter_data(
    text: str
) -> None | str:
    label, score = detect_nsfw(text)
    if label == "__label__nsfw" and score > 0.5:
        return None
    label, score = detect_toxic(text)
    if label == "__label__toxic" and score > 0.5:
        return None
    if gopher_quality_filter(text) is False:
        return None
    label, score = predict_quality(text)
    if label == "__label__low" and score > 0.5:
        return None

    text, _ = mask_phone(text)
    text, _ = mask_ip(text)
    text, _ = mask_email(text)
    return text


def process_data(
    src_path: os.PathLike,
    filtered_path: os.PathLike,
    dst_path: os.PathLike
):
    os.makedirs(filtered_path, exist_ok=True)
    os.makedirs(dst_path, exist_ok=True)
    # filter data
    total = 0
    save = 0
    with open(src_path, "rb") as fin:
        for record in ArchiveIterator(fin):
            if record.record_type != WarcRecordType.conversion:
                continue

            total += 1
            binary_text = record.reader.read()
            try:
                text = binary_text.decode(encoding=detect_encoding(binary_text))
            except (UnicodeDecodeError, LookupError, TypeError):
                continue

            filtered_text = filter_data(text)
            if filtered_text is not None:
                path = Path(filtered_path) / f"doc_{save}.txt"
                with open(path, "w", encoding="utf-8") as fout:
                    fout.write(filtered_text)

                save += 1
            if save >= 5:
                break
    print("total: ", total)
    print("save: " ,save)

    # deduplicate data
    paths = list(Path(filtered_path).glob("*.txt"))
    minihash_deduplication(paths, 32, 4, 4, 0.7, dst_path)

if __name__ == "__main__":
    PATH = "local-shared-data/furu/cs336_data/wet_files/_EnglishWetFile/2f77453343bff7bb63a2/4a897e205146ccb404d6/data.warc.wet.gz"
    filtered_path = "outputs/filtered_data"
    cleaned_path = "outputs/cleaned_data"

    parser = argparse.ArgumentParser()

    parser.add_argument("--data_path", type=str, required=False, default=PATH)
    parser.add_argument("--filtered_path", type=str, required=False, default=filtered_path)
    parser.add_argument("--cleaned_path", type=str, required=False, default=cleaned_path)

    args = parser.parse_args()
    process_data(args.data_path, args.filtered_path, args.cleaned_path)