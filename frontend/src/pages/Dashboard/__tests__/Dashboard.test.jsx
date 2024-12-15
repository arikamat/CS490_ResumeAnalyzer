import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Dashboard from '../Dashboard';
import React from 'react'; 
import { AuthProvider } from '../../../context/AuthContext';
import axios from 'axios';

jest.mock('axios');

describe('Dashboard Component', () => {
  it('displays resume fit score, matched keywords, missing keywords, and improvement suggestions', async () => {
    axios.post.mockResolvedValue({
      status: 200,
      data: {
        fit_score: 75.5,
        matched_keywords: {
          skills: ['JavaScript', 'React'],
          experience: ['Software Engineer'],
          education: ['Computer Science Degree'],
        },
        feedback: {
          missing_keywords: {
            skills: ['Node.js'],
            experience: ['5+ years in tech'],
            education: ['Masters in Computer Science'],
          },
          suggestions: {
            skills: {
              'JavaScript': 'Strengthen your JS skills.',
            },
            experience: {
              'Software Engineer': 'Work on more challenging projects.',
            },
          },
        },
      },
    });

    render(<AuthProvider><Dashboard /></AuthProvider>);

    await waitFor(() => {
      expect(screen.getByText(/Your resume matches 75.50% of the job description/i)).toBeInTheDocument();
    });

    const skillsElements = screen.getAllByText('Skills:');
    expect(skillsElements.length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText('JavaScript, React')).toBeInTheDocument();

    const experienceElements = screen.getAllByText('Experience:');
    expect(experienceElements.length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText('Software Engineer')).toBeInTheDocument();

    const educationElements = screen.getAllByText('Education:');
    expect(educationElements.length).toBeGreaterThanOrEqual(1); 
    expect(screen.getByText('Computer Science Degree')).toBeInTheDocument();

    const missingSkillsElements = screen.getAllByText('Skills:');
    expect(missingSkillsElements.length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText('Node.js')).toBeInTheDocument();

    const missingExperienceElements = screen.getAllByText('Experience:');
    expect(missingExperienceElements.length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText('5+ years in tech')).toBeInTheDocument();

    const missingEducationElements = screen.getAllByText('Education:');
    expect(missingEducationElements.length).toBeGreaterThanOrEqual(1); 
    expect(screen.getByText('Masters in Computer Science')).toBeInTheDocument();

    expect(screen.getByText('JavaScript:')).toBeInTheDocument();
    expect(screen.getByText('Strengthen your JS skills.')).toBeInTheDocument();

    const suggestionExperienceElements = screen.getAllByText('Experience:');
    expect(suggestionExperienceElements.length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText('Work on more challenging projects.')).toBeInTheDocument();

    fireEvent.change(screen.getByLabelText(/Filter by:/i), {
      target: { value: 'skills' },
    });

    await waitFor(() => {
      expect(screen.getByText('JavaScript, React')).toBeInTheDocument();
      expect(screen.queryByText('Software Engineer')).not.toBeInTheDocument();
      expect(screen.queryByText('Computer Science Degree')).not.toBeInTheDocument();
    });

    fireEvent.change(screen.getByLabelText(/Filter by:/i), {
      target: { value: 'all' },
    });

    await waitFor(() => {
      expect(screen.getByText('JavaScript, React')).toBeInTheDocument();
      expect(screen.getByText('Software Engineer')).toBeInTheDocument();
      expect(screen.getByText('Computer Science Degree')).toBeInTheDocument();
    });
  });
});
