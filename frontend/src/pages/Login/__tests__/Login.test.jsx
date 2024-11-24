import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import axios from 'axios';
import Login from '../Login'; 

jest.mock('axios');
describe('Login Component', () => {

  beforeEach(() => {
    jest.clearAllMocks();  
  });

  it('should render form with email, password input fields and submit button', () => {
    render(<Login />);

    expect(screen.getByPlaceholderText('Email')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
  });


  it('shows success text on successful login', async () => {
    axios.post.mockResolvedValueOnce({
      status: 200,
      data: { token: 'fakeToken' },
    });
  
    //mocking local storage https://stackoverflow.com/questions/32911630/how-do-i-deal-with-localstorage-in-jest-tests
    const setItemMock = jest.spyOn(Storage.prototype, 'setItem');
  
    render(<Login />);
    const user = userEvent.setup();
    await user.type(screen.getByPlaceholderText('Email'), 'jck44@example.com');
    await user.type(screen.getByPlaceholderText('Password'), 'correctpassword');
    await user.click(screen.getByRole('button', { name: /sign in/i }));
  
    expect(await screen.findByText('Login successful')).toBeInTheDocument();  
    expect(setItemMock).toHaveBeenCalledWith('token', 'fakeToken'); //check local storage set func to have been called with token
    expect(axios.post).toHaveBeenCalledWith('http://127.0.0.1:8000/api/login', {
      email: 'jck44@example.com',
      password: 'correctpassword',
    });
  });
  



  it('show error text if login failed 400 status code', async () => {
    axios.post.mockResolvedValueOnce({
      status: 400,
      data: { message: 'Invalid credentials' },
    });

    render(<Login />);
    const user = userEvent.setup();
    await user.type(screen.getByPlaceholderText('Email'), 'jck44@example.com');
    await user.type(screen.getByPlaceholderText('Password'), 'wrongpassword');
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    expect(await screen.findByText('Login failed wrong credentials')).toBeInTheDocument();
    expect(axios.post).toHaveBeenCalledWith('http://127.0.0.1:8000/api/login', {
      email: 'jck44@example.com',
      password: 'wrongpassword',
    });
    expect(axios.post).toHaveBeenCalledTimes(1);
  });

});
