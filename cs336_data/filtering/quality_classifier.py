import fasttext
import regex as re
from fastwarc import ArchiveIterator
from cs336_data.filtering.extract_context import extract_content

model = None

def predict_quality(text: str):
    global model
    if model is None:
        fasttext.load_model("local-shared-data/classifiers/lid.176.bin")
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