import fasttext
from fastwarc import ArchiveIterator
from cs336_data.filtering.extract_context import extract_content

detect_nsfw_model = fasttext.load_model("local-shared-data/classifiers/dolma_fasttext_nsfw_jigsaw_model.bin")
detect_toxic_model = fasttext.load_model("local-shared-data/classifiers/dolma_fasttext_hatespeech_jigsaw_model.bin")

def detect_nsfw(text: str):
    label, score = detect_nsfw_model.predict(text)
    return label[0], score[0]

def detect_toxic(text: str):
    label, score = detect_toxic_model.predict(text)
    return label[0], score[0]
if __name__ == "__main__":
    text = "SUCK MY C*CK WIKIPEDIA EDITORS...F*CKING *SSH*LE DORKS. "
    print(detect_nsfw(text))

    i = 0
    with open("local-shared-data/CC/example.warc.wet.gz", "rb") as f:
        for record in ArchiveIterator(f):
            html = record.reader.read()
            content = extract_content(html)
            print(content[:100])
            label1 = detect_nsfw(content)
            print(label1)
            label2 = detect_toxic(content)
            print(label2)
            print("-" * 100)
            i += 1
            if i > 20:
                break