import { generatePDF } from './generatePDF';
import jsPDF from 'jspdf';

// Mock jsPDF module
jest.mock('jspdf', () => {
  return jest.fn().mockImplementation(() => ({
    setFontSize: jest.fn(),
    setFont: jest.fn(),
    text: jest.fn(),
    setTextColor: jest.fn(),
    splitTextToSize: jest.fn().mockReturnValue(['- Example Keyword']),
    addPage: jest.fn(),
    save: jest.fn(),
  }));
});

describe('generatePDF', () => {
  it('should execute without errors', () => {
    const fitScore = 85.6;
    const matchedKeywords = {
      skills: ['JavaScript', 'React'],
      experience: ['Web Developer'],
    };
    const missingKeywords = {
      skills: ['Node.js'],
      experience: ['Backend Developer'],
    };
    const improvementSuggestions = {
      skills: {
        'JavaScript': 'Practice advanced topics',
        'React': 'Build more projects',
      },
      experience: {
        'Web Developer': 'Gain backend experience',
      },
    };

    generatePDF(fitScore, matchedKeywords, missingKeywords, improvementSuggestions);

    expect(jsPDF).toHaveBeenCalled();
  });
});
