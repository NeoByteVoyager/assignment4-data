import regex as re
from fastwarc import ArchiveIterator
from cs336_data.filtering.extract_context import extract_content

email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

ipv4_pattern = r'\b(?:25[0-5]|2[0-4]\d|1?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){3}\b'

phone_pattern = r'(?<!\d)(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{4}(?!\d)'

def mask_email(text: str) -> (str, int):
    text, count = re.subn(email_pattern, "|||EMAIL_ADDRESS|||", text)
    return text, count

def mask_phone(text: str) -> (str, int):
    text, count = re.subn(phone_pattern, "|||PHONE_NUMBER|||", text)
    return text, count

def mask_ip(text: str) -> (str, int):
    text, count = re.subn(ipv4_pattern, "|||IP_ADDRESS|||", text)
    return text, count

if __name__ == "__main__":
    PATH = "local-shared-data/CC/example.warc.gz"
    i =  0
    with open(PATH, "rb") as f:
        for record in ArchiveIterator(f):
            html = record.reader.read()
            content = extract_content(html)

            content, _ = mask_ip(content)
            content, _ = mask_phone(content)
            content, _ = mask_email(content)

            print(content)
            i += 1
            if i > 20:
                break
