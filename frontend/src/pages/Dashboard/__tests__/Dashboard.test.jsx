import { render, screen } from '@testing-library/react';
import Dashboard from '../Dashboard';

describe('Dashboard Component', () => {
  it('states resume fit score, skills, improvement', () => {
    render(<Dashboard />);

    // resume fit score sec
    expect(screen.getByText(/Resume Fit Score/i)).toBeInTheDocument();
    expect(screen.getByText(/Your resume matches 50% of the job description./i)).toBeInTheDocument();

    //sec 2
    expect(screen.getByText('Skills and Keywords Matched')).toBeInTheDocument();
    expect(screen.getByText('Strafing')).toBeInTheDocument();
    expect(screen.getByText('Aim')).toBeInTheDocument();
    expect(screen.getByText('Game sense')).toBeInTheDocument();

    //sec 3
    expect(screen.getByText('Improvement Suggestions')).toBeInTheDocument();
    expect(screen.getByText('Work on your util usage.')).toBeInTheDocument();
    expect(screen.getByText('Stop instalocking Reyna.')).toBeInTheDocument();
    expect(screen.getByText('Hit Aimlabs.')).toBeInTheDocument();
    expect(screen.getByText('Grind deathmatch.')).toBeInTheDocument();
  });
});
