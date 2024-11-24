from fastapi.testclient import TestClient
from fastapi import FastAPI
import pytest
from backend import app


client = TestClient(app)


# Test for valid data
def test_valid_user():
    """
    Tests the create_user_profile function

    Takes valid user information and stores it into the database. Ensures users can create accounts with valid input.
    """

    response = client.post(
        "/api/register",
        json={
            "email": "user@example.com",
            "password": "securePassword",
            "username": "user123",
        },
    )
    assert response.status_code == 201
    assert response.json() == {"message": "User registered"}


# test if the same email is used for 2 different users
def test_duplicate_emails():
    """
    Tests the create_user_profile function

    Takes in users with duplicate emails and attempts to make two accounts. Ensures two users cannot use the same email.
    """
    response = client.post(
        "/api/register",
        json={
            "email": "user1@example.com",
            "password": "securePassword",
            "username": "user123",
        },
    )

    response_duplicate = client.post(
        "/api/register",
        json={
            "email": "user1@example.com",
            "password": "otherSecurePassword",
            "username": "user321",
        },
    )
    assert response_duplicate.status_code == 400
    assert response_duplicate.json() == {"detail": "Email is not unique"}
