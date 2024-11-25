import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../../App.jsx';


describe('App Routing Tests', () => {

    const renderWithRoute = (initialRoute) => {
        window.history.pushState({}, 'Test page', initialRoute);
        render(
            <App />
        );
    };
    
    it('renders Home page at root ("/")', () => {
        renderWithRoute('/');
        expect(screen.getByText("AI-Powered Resume Analyzer and Job Matcher")).toBeInTheDocument();
    });

    it('renders Login page at "/login"', () => {
        renderWithRoute('/login');
        expect(screen.getByText("Sign in")).toBeInTheDocument();
    });

    it('renders SignUp page at "/register"', () => {
        renderWithRoute('/register');
        expect(screen.getByText("Create an Account")).toBeInTheDocument();
    });

    it('redirects unauthenticated users from "/upload" to "/login"', () => {
        renderWithRoute('/upload');
        expect(screen.getByText("Sign in")).toBeInTheDocument();
    });

    it('redirects unauthenticated users from "/dashboard" to "/login"', () => {
        renderWithRoute('/dashboard');
        expect(screen.getByText("Sign in")).toBeInTheDocument();
    });
    
});