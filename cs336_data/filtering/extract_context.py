from fastwarc import ArchiveIterator
from resiliparse.parse.encoding import detect_encoding
from resiliparse.extract.html2text import extract_plain_text

def extract_content(html:bytes) -> str | None:
    encoding = detect_encoding(html)
    html_str = html.decode(encoding)

    content = extract_plain_text(html_str)
    return content

if __name__ == "__main__":
    i = 0
    with open("local-shared-data/CC/example.warc.gz", "rb") as f:
        for record in ArchiveIterator(f):
            html = record.reader.read()
            content = extract_content(html)
            print(content)
            i += 1
            if i > 8:
                break
    print('-' * 80)
    i = 0
    with open("local-shared-data/CC/example.warc.wet.gz", "rb") as f:
        for record in ArchiveIterator(f):
            html = record.reader.read()
            print(html.decode(detect_encoding(html)))

            i += 1
            if i > 3:
                break