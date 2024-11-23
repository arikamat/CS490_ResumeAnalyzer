
from fastapi.testclient import TestClient
from fastapi import FastAPI
import pytest
from backend.main import app



client = TestClient(app)
# Test for valid data
def test_valid_user():
    response = client.post("/api/register", json={
        "email": "user@example.com",
        "password": "securePassword",
        "username": "user123"
    })
    assert response.status_code == 201
    assert response.json() == {"message": "User registered"}

#test if the same email is used for 2 different users
def test_duplicate_emails():
    response = client.post("/api/register", json={
        "email": "user@example.com",
        "password": "securePassword",
        "username": "user123"
    })

    response_duplicate = client.post("/api/register", json={
        "email": "user@example.com",
        "password": "otherSecurePassword",
        "username": "user321"
    })
    assert response.status_code == 400
    assert response.json() == {"detail":"Email is not unique"}
