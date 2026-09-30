import fasttext
import regex as re
from cs336_data.filtering.extract_context import extract_content
from fastwarc import ArchiveIterator

model = None

def predict_language(sentence):
    global model
    if model is None:
        model = fasttext.load_model("local-shared-data/classifiers/lid.176.bin")
    sentence = re.sub("\\n", "", sentence)
    label, prob = model.predict(sentence)
    return label[0], prob[0]

if __name__ == "__main__":
    '''
    PATH = "local-shared-data/CC/example.warc.gz"
    i = 0
    with open(PATH, "rb") as f:
        for record in ArchiveIterator(f):
            html = record.reader.read()
            content = extract_content(html)
            #print(content[:100])
            print(predict_language(content))
            #print("-" * 80)
            i += 1
            if i > 20:
                break
    '''
    label = predict_language("你真的很nice，good, beautiful")
    print(label)