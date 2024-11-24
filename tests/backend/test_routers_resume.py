from fastapi.testclient import TestClient
from fastapi import FastAPI
import pytest
from backend import app
from pathlib import Path
from backend.db import resume_database
client = TestClient(app)
TESTDIR = Path(__file__).parent / "test_files"

JWT_HEADER = {"Authorization": "Bearer valid_jwt"}

def test_resume_upload_valid_pdf():
    f = open(TESTDIR / "test_pdf_1.pdf","rb")
    res = client.post("/api/resume-upload",
                      files={"resume_file": ("test_resume.pdf", f, "application/pdf")},
                      headers={"Authorization": "Bearer valid_jwt"}
                      )
    assert res.status_code == 200
    assert res.json() == {"message": "Resume uploaded successfully."}
    assert "Lorem" in resume_database["valid_jwt"]

def test_resume_upload_valid_docx():
    f = open(TESTDIR / "test_docx_1.docx","rb")
    res = client.post("/api/resume-upload",
                      files={"resume_file": ("test_resume.pdf", f, "application/pdf")},
                      headers={"Authorization": "Bearer valid_jwt"}
                      )
    assert res.status_code == 200
    assert res.json() == {"message": "Resume uploaded successfully."}