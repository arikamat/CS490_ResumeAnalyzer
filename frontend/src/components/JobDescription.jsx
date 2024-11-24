import { useState } from 'react';
import './JobDescription.css';
import axios from 'axios';

const JobDescription = () => {
  const [text, setText] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const charLimit = 5000;

  const handleChange = (e) => {
    setText(e.target.value)
  }

  const getRemainingCharacters = () => {
    return charLimit - text.length;
  }

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

  const handleSubmit = async (e) => {
    e.preventDefault();

    setSuccess('');
    setError('');

    if (text.length > charLimit) {
        setError('Character limit exceeded');
        return;
    }

    try {
        const response = await axios.post('/api/job-description', { description: text });

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
