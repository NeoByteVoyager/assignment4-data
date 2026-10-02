import argparse
from fastwarc import ArchiveIterator,WarcRecordType
from resiliparse.parse.encoding import detect_encoding
from resiliparse.extract.html2text import extract_plain_text

def extract_content(html:bytes) -> str | None:
    try:
        html_str = html.decode(detect_encoding(html))
    except (UnicodeDecodeError, LookupError, TypeError):
        return None

    content = extract_plain_text(html_str)
    return content

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--path", type=str, default="local-shared-data/CC/example.warc.gz", required=False)

    args = parser.parse_args()

    with open(args.path, "rb") as f:
        for record in ArchiveIterator(f):
            if record.record_type != WarcRecordType.response:
                continue
            print(record.http_headers.status_code)
            if record.http_headers.status_code != 200:
                continue
            html = record.reader.read()
            content = extract_content(html)
            #print(content)

            print('-' * 80)
