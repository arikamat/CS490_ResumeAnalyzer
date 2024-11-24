import { useState } from 'react'
import './FileUpload.css'
import axios from 'axios';

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = (e) => {
    const selectedFile = e.target.files[0];
    
    if (!selectedFile) return;

    if (selectedFile.type !== 'application/pdf') {
      setError('File must be a PDF');
      setSuccess('');
      setFile(null);
      return
    }

    if (selectedFile.size > 2 * 1024 * 1024) {
      setError('File size must be under 2 MB');
      setSuccess('');
      setFile(null);
      return;
    }

    setError('');
    setFile(selectedFile);
    setSuccess('File is ready to upload');
  }

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!file) {
      setError('Please select a valid PDF before submitting');
      setSuccess('');
      return
    }
    
    setSuccess('File is ready to upload');
    setError('');
  }


  return (
    <div className="file-upload">
        <form onSubmit={handleSubmit}>
          <h1>Resume File Upload</h1>

          <div className='input-container'>
            <input 
              type="file" 
              onChange={handleChange}
            />  
            <button type="submit">Upload</button>
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
