import React from 'react';
import { render, screen, waitFor,fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import axios from 'axios';
import SignUp from '../SignUp';
import { AuthProvider } from '../../../context/AuthContext';
import { MemoryRouter, Routes, Route } from "react-router-dom";
jest.mock('axios');
describe('SignUp Component', () => {

  //mocks are persistent so need to be cleared (i think)
  beforeEach(() => {
    jest.clearAllMocks();
  });

  //inside it is what I expect to happen and what will be verified 
  it('should render form w/ all input fields and submit button', () => {
    render(
      <AuthProvider>
        <MemoryRouter initialEntries={["/register"]}>
          <Routes>
            <Route path="/register" element={<SignUp />} />
            <Route path="/login" element={<div>Login</div>} />
          </Routes>
        </MemoryRouter>
      </AuthProvider>
    );

    expect(screen.getByPlaceholderText('Email')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Username')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Password')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Confirm Password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign up/i })).toBeInTheDocument(); //i use regular expression to match
  });

  //needs to be reviewed 
  it('show text if passwords do not match', async () => {
    render(
      <AuthProvider>
        <MemoryRouter initialEntries={["/register"]}>
          <Routes>
            <Route path="/register" element={<SignUp />} />
            <Route path="/login" element={<div>Login</div>} />
          </Routes>
        </MemoryRouter>
      </AuthProvider>
    );
    const user = userEvent.setup();
    //use awaits to make sure jest does not proceed due to promise 
    await user.type(screen.getByPlaceholderText('Email'), 'jck44@example.com');
    await user.type(screen.getByPlaceholderText('Username'), 'jeremy');
    await user.type(screen.getByPlaceholderText('Password'), 'safwanbad');
    await user.type(screen.getByPlaceholderText('Confirm Password'), 'wrongpass');
    await user.click(screen.getByRole('button', { name: /sign up/i }));

    expect(await screen.findByText('Passwords do not match')).toBeInTheDocument();
    //? correct when "Signup failed email is not unique"
  });

  it('send post request and show change page on successful signup', async () => {
    //mock a response 
    axios.post.mockResolvedValueOnce({
      status: 201,
      data: { message: 'User registered' },
    });

    render(
      <AuthProvider>
        <MemoryRouter initialEntries={["/register"]}>
          <Routes>
            <Route path="/register" element={<SignUp />} />
            <Route path="/login" element={<div>Login</div>} />
          </Routes>
        </MemoryRouter>
      </AuthProvider>
    );
    const user = userEvent.setup();
    await user.type(screen.getByPlaceholderText('Email'), 'jck44@example.com');
    await user.type(screen.getByPlaceholderText('Username'), 'jeremy');
    await user.type(screen.getByPlaceholderText('Password'), 'safwanbad');
    await user.type(screen.getByPlaceholderText('Confirm Password'), 'safwanbad');
    await user.click(screen.getByRole('button', { name: /sign up/i }));

    // check for success text
    expect(screen.getByText('Login')).toBeInTheDocument();

    //check it calls correct location, with correct data, and that it calls it only once
    expect(axios.post).toHaveBeenCalledWith('http://127.0.0.1:8000/api/register', {
      email: 'jck44@example.com',
      username: 'jeremy',
      password: 'safwanbad',
    });
    expect(axios.post).toHaveBeenCalledTimes(1);
  });

  it('shows error text if signup fails due to 400 status code', async () => {
    axios.post.mockResolvedValueOnce({
      status: 400,
      data: { message: 'Email is not unique' },
    });

    render(
      <AuthProvider>
        <MemoryRouter initialEntries={["/register"]}>
          <Routes>
            <Route path="/register" element={<SignUp />} />
            <Route path="/login" element={<div>Login</div>} />
          </Routes>
        </MemoryRouter>
      </AuthProvider>
    );
    const user = userEvent.setup();
    await user.type(screen.getByPlaceholderText('Email'), 'jck44@example.com');
    await user.type(screen.getByPlaceholderText('Username'), 'jeremy');
    await user.type(screen.getByPlaceholderText('Password'), 'safwanbad');
    await user.type(screen.getByPlaceholderText('Confirm Password'), 'safwanbad');
    await user.click(screen.getByRole('button', { name: /sign up/i }));

    expect(await screen.findByText('Signup failed email is not unique')).toBeInTheDocument();

    // Check that axios.post was called with the correct parameters
    expect(axios.post).toHaveBeenCalledWith('http://127.0.0.1:8000/api/register', {
      email: 'jck44@example.com',
      username: 'jeremy',
      password: 'safwanbad',
    });

    // Check that axios.post was called only once
    expect(axios.post).toHaveBeenCalledTimes(1);
  });
  it('displays loading component while the signup request is in progress', async () => {
    //set timeout for entire test 
    jest.setTimeout(10000);


    axios.post.mockImplementation(() =>
      new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            status: 201,
            data: { message: 'User registered' }
          }); //make it sucess
        }, 1000); // give one second delay
      })
    );

    render(
      <AuthProvider>
        <MemoryRouter initialEntries={["/register"]}>
          <Routes>
            <Route path="/register" element={<SignUp />} />
            <Route path="/login" element={<div>Login</div>} />
          </Routes>
        </MemoryRouter>
      </AuthProvider>
    );
    const user = userEvent.setup();

    await user.type(screen.getByPlaceholderText('Email'), 'jck44@example.com');
    await user.type(screen.getByPlaceholderText('Username'), 'jeremy');
    await user.type(screen.getByPlaceholderText('Password'), 'safwanbad');
    await user.type(screen.getByPlaceholderText('Confirm Password'), 'safwanbad');
    fireEvent.click(screen.getByRole('button', { name: /sign up/i })); //trigger with fireEvent so no delay i dont want full process

    expect(screen.getByText('Loading...')).toBeInTheDocument(); // find loading to appear immedietely 

    await waitFor(() => expect(screen.queryByText('Loading...')).not.toBeInTheDocument(), { timeout: 1500 }); //WAIT for loading to stop after succeess
    expect(screen.getByText('Login')).toBeInTheDocument(); //find end message
  });

  it('shows custom error message signup', async () => {
    axios.post.mockRejectedValueOnce({
      response: {
        status: 400,
        data: { detail: 'custom error' },
      },
    });


    render(<SignUp />);
    const user = userEvent.setup();
    await user.type(screen.getByPlaceholderText('Email'), 'jck44@example.com');
    await user.type(screen.getByPlaceholderText('Username'), 'jeremy');
    await user.type(screen.getByPlaceholderText('Password'), 'safwanbad');
    await user.type(screen.getByPlaceholderText('Confirm Password'), 'safwanbad');
    await user.click(screen.getByRole('button', { name: /sign up/i }));

    expect(await screen.findByText('custom error')).toBeInTheDocument();

    
  });


});
