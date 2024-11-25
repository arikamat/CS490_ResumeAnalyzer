import { useState } from 'react'
import './FileUpload.css'
import axios from 'axios';
import React from 'react';

// Main component for handling file upload functionality
function FileUpload(){
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Handles file selection and validation when the user chooses a file
  const handleChange = (e) => {
    const selectedFile = e.target.files[0];

    setError('');
    setSuccess('');
    
    if (!selectedFile) return;

    if (selectedFile.type !== 'application/pdf') {
      setError('File must be a PDF');
      setFile(null);
      return;
    }

    if (selectedFile.size > 2 * 1024 * 1024) {
      setError('File size must be under 2 MB');
      setFile(null);
      return;
    }

    setFile(selectedFile);
    setSuccess('File is ready to upload');
  }

  // Handles form submission, sending the selected file to the server
  const handleSubmit = async (e) => {
    e.preventDefault();

    setSuccess('');
    setError('');

    if (!file) {
      setError('Please select a valid PDF before submitting');
      return;
    }
    
    // Prepare FormData object to send the file to the server
    const formData = new FormData();
    formData.append('resume_file', file);

    // Attempt to upload the file using axios
    try {
      const jwtToken="test"
      const url = 'http://127.0.0.1:8000/api/resume-upload';
      const payload = formData;
      const config = {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${jwtToken}`,
        },
      };
  
      const response = await axios.post(url, payload, config);

      if (response.status === 200) {
        setSuccess('File uploaded successfully!');
      }
      else {
        setError('Failed to upload the file.');
      }

    }
    catch (err) {
      setError('An error occurred during file upload.');
      setSuccess('');
    }
  }

  // Page layout and JSX structure for file upload form
  return (
    <div className="file-upload">
        <form onSubmit={handleSubmit}>
          <h1>Resume File Upload</h1>

          <div className='input-container'>
            <label htmlFor="file-input">Upload File:</label>
            <input 
              aria-label="Upload File"
              id="file-input"
              type="file" 
              onChange={handleChange}
            />  
        <button 
          type="submit"
          disabled={!file || error}
          >Upload
        </button>

          </div>

          <div className='message-container'>
            {error && <p className="error">{error}</p>}
            {success && <p className="success">{success}</p>}
          </div>

        </form>
    </div>
  );
}

export default FileUpload