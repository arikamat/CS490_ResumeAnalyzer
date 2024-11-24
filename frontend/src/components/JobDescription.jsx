import { useState } from 'react';
import './JobDescription.css';
import axios from 'axios';

const JobDescription = () => {
  const [text, setText] = useState('');
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

  const handleSubmit = (e) => {
    e.preventDefault();
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
            <button type="submit">Upload</button>
          </div>
          <div className='char-info'>
            <p>{text.length} / {charLimit} characters</p>
            {getCharacterWarning()}
            {getRemainingCharacters() >= 0 && (
                <p>{getRemainingCharacters()} characters remaining</p>
            )}
          </div>
        </form>
    </div>
  );
}

export default JobDescription
