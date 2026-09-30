from fastwarc import ArchiveIterator, WarcRecordType


i = 0
PATH = "local-shared-data/CC/example.warc.gz"
with open(PATH, "rb") as f:
    for record in ArchiveIterator(f):
        print(record.record_type, record.content_length)

        html = record.reader.read()
        print(html)
        i += 1
        if i > 10:
          break