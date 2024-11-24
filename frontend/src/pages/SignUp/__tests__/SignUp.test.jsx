import { render, screen } from '@testing-library/react';
import SignUp from '../SignUp';
import React from 'react';


describe('SignUp Component', () => {
  it('renders SignUp form with required fields', () => {
    render(<SignUp />);
    expect(screen.getByPlaceholderText('Email')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Username')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Password')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Confirm Password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Sign Up/i })).toBeInTheDocument();
  });
});
