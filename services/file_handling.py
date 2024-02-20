import os
import sys

BOOK_PATH = 'book/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}


def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    end_sings = ',.!:;?'
    count = 0
    if len(text) < start + size:
        size = len(text) - start
        text = text[start:]
    else:
        if text[start + size] == '.' and text[start + size - 1] in end_sings:
            text = text[start:start + size - 2]
            size -= 2
        else:
            text = text[start: start + size]
        for i in range(size - 1, 0, -1):
            if text[i] in end_sings:
                break
            count = size - i
    page_text = text[:size - count]
    page_size = size - count
    return page_text, page_size


def prepare_book(path: str) -> None:
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read()
    start, page = 0, 1
    while start < len(text):
        page_text, page_size = _get_part_text(text, start, PAGE_SIZE)
        book[page] = page_text.strip()
        start += page_size
        page += 1


prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))
