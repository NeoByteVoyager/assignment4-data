import fasttext
import regex as re
from fastwarc import ArchiveIterator
from cs336_data.filtering.extract_context import extract_content

model = fasttext.load_model("outputs/quality_classifier.bin")

def predict_quality(text: str):
    text = re.sub("\n", "", text)
    labels, scores = model.predict(text)
    return labels[0], scores[0]

if __name__ == "__main__":
    i = 0
    with open("local-shared-data/CC/example.warc.gz", "rb") as f:
        for record in ArchiveIterator(f):
            html = record.reader.read()

            content = extract_content(html)

            labels, score = predict_quality(content)
            print(labels, score)

            i += 1
            if i >= 6:
                break