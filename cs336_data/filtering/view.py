from fastwarc import ArchiveIterator, WarcRecordType
from resiliparse.parse.encoding import detect_encoding

i = 0
# PATH = "local-shared-data/CC/example.warc.gz"
PATH = "local-shared-data/furu/cs336_data/wet_files/_EnglishWetFile/2f77453343bff7bb63a2/4a897e205146ccb404d6/data.warc.wet.gz"
with open(PATH, "rb") as f:
    for record in ArchiveIterator(f):
        print(record.record_type, record.content_length)

        html = record.reader.read()
        text = html.decode(detect_encoding(html))
        print(text)
        i += 1
        if i > 10:
          break