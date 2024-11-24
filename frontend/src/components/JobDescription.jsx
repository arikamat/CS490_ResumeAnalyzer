import { useState } from 'react';
import './JobDescription.css';
import axios from 'axios';

// Component for handling job description text upload
const JobDescription = () => {
  const [text, setText] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const charLimit = 5000;

  // Update text state when input changes
  const handleChange = (e) => {
    setText(e.target.value)
  }

  // Calculate remaining characters
  const getRemainingCharacters = () => {
    return charLimit - text.length;
  }

  // Display warning based on remaining characters
  const getCharacterWarning = () => {
    const remaining = getRemainingCharacters();
    if (remaining < 0) {
        return <p className='warning-exceed'>Character limit exceeded</p>
    }
    else if (remaining <= 100) {
        return <p className='warning-approach'>You are almost at the character limit</p>
    }
    return null
  }

  // Handle form submission and upload the text
  const handleSubmit = async (e) => {
    e.preventDefault();

    setSuccess('');
    setError('');

    if (text.length > charLimit) {
        setError('Character limit exceeded');
        return;
    }

    // Attempt to upload the text using axios
    try {
        url = 'http://127.0.0.1:8000/api/job-description';
        const response = await axios.post(url, { description: text });

        if (response.status === 200) {
            setSuccess('Job description uploaded successfully!');
            setText('');
          }
          else {
            setError('Failed to upload job description.');
          }
    
    }
    catch (err) {
        setError('An error occurred during submission.');
    }

  }

  // Page layout and JSX structure for text upload form
  return (
    <div className="job-description">
        <form onSubmit={handleSubmit}>
          <h1>Job Description</h1>
          <div className='input-container'>
            <textarea
                value={text}
                onChange={handleChange}
                placeholder="Enter job description here..."
            />
            <button 
                type="submit"
                disabled={!text || text.length > charLimit}
                >Upload
            </button>
          </div>
          <div className='char-info'>
            <p>{text.length} / {charLimit} characters</p>
            {getCharacterWarning()}
            {getRemainingCharacters() >= 0 && (
                <p>{getRemainingCharacters()} characters remaining</p>
            )}
          </div>
          <div className='message-container'>
            {error && <p className="error">{error}</p>}
            {success && <p className="success">{success}</p>}
          </div>
        </form>
    </div>
  );
}

export default JobDescription
