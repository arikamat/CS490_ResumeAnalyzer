from fastapi.testclient import TestClient
from fastapi import FastAPI
import pytest
from backend import app


client = TestClient(app)


# Test for valid login credentials
def test_valid_user():
    '''
    Tests the check_login function

    Creates a valid user and attempts to login in successfully
    '''

    response = client.post(
        "/api/register",
        json={
            "email": "user5@example.com",
            "password": "securePassword",
            "username": "user123",
        },
    )

    login = client.post(
        "/api/login",
        json={
            "email": "user5@example.com",
            "password": "securePassword",
        },
    )
    assert login.status_code == 200
    assert login.json()["token"] #if the token is not empty and it was generated
    


# Test for trying to login with a non-registered email
def test_registered_email():
    '''
    Tests the check_login function

    Ensures that login is not possible without first creating an account
    '''

    login = client.post(
        "/api/login",
        json={
            "email": "thisEmailIsNotRegistered@example.com",
            "password": "securePassword",
        },
    )
    assert login.status_code == 400
    assert login.json() == {"detail": "No account associated with this email"}


# Test for trying to login with the wrong password
def test_incorrect_password():
    '''
    Tests the check_login function

    Ensures that login is not possible without the correct password
    '''

    response = client.post(
        "/api/register",
        json={
            "email": "wrongPassword@example.com",
            "password": "securePassword",
            "username": "user123",
        },
    )

    login = client.post(
        "/api/login",
        json={
            "email": "wrongPassword@example.com",
            "password": "securePasswordWrong",
        },
    )

    assert login.status_code == 400
    assert login.json() == {"detail": "Incorrect password"}
 


