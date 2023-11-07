import re


def clean_text(text):
    num, text = text.split("_", maxsplit=1)
    return f"{int(num):>2}) {text.replace('_', ' ').capitalize()}"


def extract_leading_numbers(text):
    m = re.match(r"^\d+", text)
    if m:
        return int(m.group())
