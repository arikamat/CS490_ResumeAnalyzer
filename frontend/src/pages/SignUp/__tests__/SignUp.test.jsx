import React from 'react';
import { render, screen, waitFor  } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import axios from 'axios';
import SignUp from '../SignUp';

jest.mock('axios');
describe('SignUp Component', () => {

  //mocks are persistent so need to be cleared (i think)
  beforeEach(() => {
    jest.clearAllMocks();
  });

  //inside it is what I expect to happen and what will be verified 
  it('should render form w/ all input fields and submit button', () => {
    render(<SignUp />);
    expect(screen.getByPlaceholderText('Email')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Username')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Password')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Confirm Password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign up/i })).toBeInTheDocument(); //i use regular expression to match
  });

  //needs to be reviewed 
  it('show text if passwords do not match', async () => {
    render(<SignUp />);
    const user = userEvent.setup(); 
    //use awaits to make sure jest does not proceed due to promise 
    await user.type(screen.getByPlaceholderText('Email'), 'jck44@example.com');
    await user.type(screen.getByPlaceholderText('Username'), 'jeremy');
    await user.type(screen.getByPlaceholderText('Password'), 'safwanbad');
    await user.type(screen.getByPlaceholderText('Confirm Password'), 'safwanbad');
    await user.click(screen.getByRole('button', { name: /sign up/i }));
    
    expect(await screen.findByText('Passwords do not match')).toBeInTheDocument();
    //? correct when "Signup failed email is not unique"
  });

  it('send post request and show success text on successful signup', async () => {
    //mock a response 
    axios.post.mockResolvedValueOnce({
      status: 201,
      data: { message: 'User registered' }, 
    });

    render(<SignUp />);
    const user = userEvent.setup();
    await user.type(screen.getByPlaceholderText('Email'), 'jck44@example.com');
    await user.type(screen.getByPlaceholderText('Username'), 'jeremy');
    await user.type(screen.getByPlaceholderText('Password'), 'safwanbad');
    await user.type(screen.getByPlaceholderText('Confirm Password'), 'safwanbad');
    await user.click(screen.getByRole('button', { name: /sign up/i }));

    // check for success text
    expect(await screen.findByText('Signup completed')).toBeInTheDocument();

    //check it calls correct location, with correct data, and that it calls it only once
    expect(axios.post).toHaveBeenCalledWith('/api/register', {
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
  
    render(<SignUp />);
    const user = userEvent.setup();
    await user.type(screen.getByPlaceholderText('Email'), 'jck44@example.com');
    await user.type(screen.getByPlaceholderText('Username'), 'jeremy');
    await user.type(screen.getByPlaceholderText('Password'), 'safwanbad');
    await user.type(screen.getByPlaceholderText('Confirm Password'), 'safwanbad');
    await user.click(screen.getByRole('button', { name: /sign up/i }));
 
    expect(await screen.findByText('Signup failed email is not unique')).toBeInTheDocument();
  
    // Check that axios.post was called with the correct parameters
    expect(axios.post).toHaveBeenCalledWith('/api/register', {
      email: 'jck44@example.com',
      username: 'jeremy',
      password: 'safwanbad',
    });
  
    // Check that axios.post was called only once
    expect(axios.post).toHaveBeenCalledTimes(1);
  });  
});
