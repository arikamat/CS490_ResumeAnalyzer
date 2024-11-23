import pytest
from pathlib import Path
import io
import sys
from backend.utils import extract_text_from_pdf, extract_text_from_docx

TESTDIR = Path(__file__).parent / "test_files"

def test_extract_text_from_pdf():
    pdf_file = TESTDIR/"test_pdf_1.pdf"
    expect_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed feugiat arcu tempus, interdum tellus non, aliquam nulla. Morbi tristique augue nec vulputate dictum. Etiam posuere lorem at lectus scelerisque feugiat. Suspendisse porta ante a elit malesuada, et viverra turpis suscipit. Maecenas fringilla nec arcu et sagittis. Vivamus dignissim ligula ac diam cursus faucibus. Suspendisse felis odio, tristique quis ultricies eget, dictum sit amet lectus. Fusce diam nisi, vulputate id laoreet ut, vehicula at lorem. Fusce malesuada turpis velit, et pulvinar neque bibendum eget. Curabitur rutrum leo ac accumsan congue. Sed porta, justo ac venenatis auctor, velit est fringilla leo, luctus fermentum ex risus a nulla. Aliquam volutpat nunc vel auctor vehicula. Nullam tempor eleifend purus. Interdum et malesuada fames ac ante ipsum primis in faucibus. Ut finibus scelerisque varius."
    f = open(pdf_file,"rb")
    data = f.read()
    f.close()
    stream = io.BytesIO(data)

    actual = extract_text_from_pdf(stream)
    assert actual == expect_text

def test_extract_text_from_docx():
    docx_file = TESTDIR/"test_docx_1.docx"
    expect_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed feugiat arcu tempus, interdum tellus non, aliquam nulla. Morbi tristique augue nec vulputate dictum. Etiam posuere lorem at lectus scelerisque feugiat. Suspendisse porta ante a elit malesuada, et viverra turpis suscipit. Maecenas fringilla nec arcu et sagittis. Vivamus dignissim ligula ac diam cursus faucibus. Suspendisse felis odio, tristique quis ultricies eget, dictum sit amet lectus. Fusce diam nisi, vulputate id laoreet ut, vehicula at lorem. Fusce malesuada turpis velit, et pulvinar neque bibendum eget. Curabitur rutrum leo ac accumsan congue. Sed porta, justo ac venenatis auctor, velit est fringilla leo, luctus fermentum ex risus a nulla. Aliquam volutpat nunc vel auctor vehicula. Nullam tempor eleifend purus. Interdum et malesuada fames ac ante ipsum primis in faucibus. Ut finibus scelerisque varius."
    f = open(docx_file,"rb")
    data = f.read()
    f.close()
    stream = io.BytesIO(data)

    actual = extract_text_from_docx(stream)

    assert actual == expect_text