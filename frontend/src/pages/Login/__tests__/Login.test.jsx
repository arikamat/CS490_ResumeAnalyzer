import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import axios from 'axios';
import Login from '../Login';
import { AuthProvider } from '../../../context/AuthContext';
import { MemoryRouter, Routes, Route } from "react-router-dom";
jest.mock('axios');
describe('Login Component', () => {

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should render form with email, password input fields and submit button', () => {
    render(
      <AuthProvider>
        <MemoryRouter initialEntries={["/login"]}>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/upload" element={<div>Upload</div>} />
          </Routes>
        </MemoryRouter>
      </AuthProvider>
    );

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

    render(
      <AuthProvider>
        <MemoryRouter initialEntries={["/login"]}>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/upload" element={<div>Upload</div>} />
          </Routes>
        </MemoryRouter>
      </AuthProvider>
    );
    const user = userEvent.setup();
    await user.type(screen.getByPlaceholderText('Email'), 'jck44@example.com');
    await user.type(screen.getByPlaceholderText('Password'), 'correctpassword');
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    // expect(await screen.findByText('Login successful')).toBeInTheDocument();
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

    render(
      <AuthProvider>
        <MemoryRouter initialEntries={["/login"]}>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/upload" element={<div>Upload</div>} />
          </Routes>
        </MemoryRouter>
      </AuthProvider>
    );
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

  it('displays loading component while the login request is in progress', async () => {
    //set timeout for entire test 
    jest.setTimeout(10000); 
  
    const mockResponse = { data: { token: 'fakeToken' } }; // give fake token to pass
    axios.post.mockImplementation(() =>
      new Promise((resolve) => {
        setTimeout(() => {
          resolve({ status: 200, data: mockResponse }); //make it sucess
        }, 1000); // give one second delay
      })
    );
    render(
      <AuthProvider>
        <MemoryRouter initialEntries={["/login"]}>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/upload" element={<div>Upload</div>} />
          </Routes>
        </MemoryRouter>
      </AuthProvider>
    );
    const user = userEvent.setup();
  

    await user.type(screen.getByPlaceholderText('Email'), 'jck44@example.com');
    await user.type(screen.getByPlaceholderText('Password'), 'correctpassword');
    fireEvent.click(screen.getByRole('button', { name: /sign in/i })); //trigger with fireEvent so no delay i dont want full process
  
    expect(screen.getByText('Loading...')).toBeInTheDocument(); // find loading to appear immedietely 
  
    await waitFor(() => expect(screen.queryByText('Loading...')).not.toBeInTheDocument(), { timeout: 1500 }); //WAIT for loading to stop after succeess
    // expect(screen.getByText('Login successful')).toBeInTheDocument(); //find end message
    expect(screen.getByText('Upload')).toBeInTheDocument();
  });
  

});
