from fastapi.testclient import TestClient
from fastapi import FastAPI
import pytest
from backend import app
from pathlib import Path
from backend.db import resume_jobdescrip_db

client = TestClient(app)
TESTDIR = Path(__file__).parent / "test_files"

JWT_HEADER = {"Authorization": "Bearer valid_jwt"}
EXPECTED_TEXT = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed feugiat arcu tempus, interdum tellus non, aliquam nulla. Morbi tristique augue nec vulputate dictum. Etiam posuere lorem at lectus scelerisque feugiat. Suspendisse porta ante a elit malesuada, et viverra turpis suscipit. Maecenas fringilla nec arcu et sagittis. Vivamus dignissim ligula ac diam cursus faucibus. Suspendisse felis odio, tristique quis ultricies eget, dictum sit amet lectus. Fusce diam nisi, vulputate id laoreet ut, vehicula at lorem. Fusce malesuada turpis velit, et pulvinar neque bibendum eget. Curabitur rutrum leo ac accumsan congue. Sed porta, justo ac venenatis auctor, velit est fringilla leo, luctus fermentum ex risus a nulla. Aliquam volutpat nunc vel auctor vehicula. Nullam tempor eleifend purus. Interdum et malesuada fames ac ante ipsum primis in faucibus. Ut finibus scelerisque varius."


def test_resume_upload_valid_pdf():
    """
    Tests resume-upload endpoint by uploading a valid pdf file to ensure appropriate parsing and behavior
    """
    f = open(TESTDIR / "test_resume_pdf1.pdf", "rb")
    res = client.post(
        "/api/resume-upload",
        files={"resume_file": ("test_resume_pdf1.pdf", f, "application/pdf")},
        headers=JWT_HEADER,
    )
    f.close()
    assert res.status_code == 200
    assert res.json() == {"message": "Resume uploaded successfully."}
    assert resume_jobdescrip_db["valid_jwt"]["resume_text"] == EXPECTED_TEXT


def test_resume_upload_valid_pdf_jwt_doesnt_exist():
    """
    Tests resume-upload endpoint by uploading a valid pdf file when database doesn't have jwt in it
    """
    f = open(TESTDIR / "test_resume_pdf1.pdf", "rb")
    res = client.post(
        "/api/resume-upload",
        files={"resume_file": ("test_resume_pdf1.pdf", f, "application/pdf")},
        headers={"Authorization": "Bearer new_jwt"},
    )
    f.close()
    assert res.status_code == 200
    assert res.json() == {"message": "Resume uploaded successfully."}
    assert resume_jobdescrip_db["new_jwt"]["resume_text"] == EXPECTED_TEXT


def test_resume_upload_valid_docx():
    """
    Tests resume-upload endpoint by uploading a valid docx file to ensure appropriate parsing and behavior
    """
    f = open(TESTDIR / "test_resume_docx1.docx", "rb")
    res = client.post(
        "/api/resume-upload",
        files={
            "resume_file": (
                "test_resume_docx1.docx",
                f,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
        headers=JWT_HEADER,
    )
    f.close()
    assert res.status_code == 200
    assert res.json() == {"message": "Resume uploaded successfully."}
    assert resume_jobdescrip_db["valid_jwt"]["resume_text"] == EXPECTED_TEXT


def test_resume_upload_invalid_file():
    """
    Tests resume-upload endpoint by uploading a text file to ensure appropriate error response
    """
    f = open(TESTDIR / "test_resume_txt1.txt", "rb")
    res = client.post(
        "/api/resume-upload",
        files={"resume_file": ("test_resume_txt1.txt", f, "text/plain")},
        headers=JWT_HEADER,
    )
    f.close()
    assert res.status_code == 400
    assert res.json() == {
        "detail": "Invalid file type. Only PDF or DOCX files are allowed."
    }


def test_resume_upload_large_file():
    """
    Tests resume-upload endpoint by uploading a file larger than 2MB to ensure appropriate error response
    """
    f = open(TESTDIR / "test_large_pdf1.pdf", "rb")
    res = client.post(
        "/api/resume-upload",
        files={"resume_file": ("test_large_pdf1.pdf", f, "application/pdf")},
        headers=JWT_HEADER,
    )
    f.close()
    assert res.status_code == 400
    assert res.json() == {"detail": "File size is over 2MB."}


def test_resume_upload_jwt_err():
    """
    Tests resume-upload endpoint without Authorization to check appropriate error response
    """
    f = open(TESTDIR / "test_resume_pdf1.pdf", "rb")
    res = client.post(
        "/api/resume-upload",
        files={"resume_file": ("test_resume_pdf1.pdf", f, "application/pdf")},
    )
    f.close()
    assert res.status_code == 400
    assert res.json() == {"detail": "Error with JWT"}
