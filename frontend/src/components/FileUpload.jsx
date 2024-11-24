import { useState } from 'react'
import './FileUpload.css'
import axios from 'axios';

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = (e) => {
    const selectedFile = e.target.files[0];

    setError('');
    setSuccess('');
    
    if (!selectedFile) return;

    if (selectedFile.type !== 'application/pdf') {
      setError('File must be a PDF');
      setFile(null);
      return
    }

    if (selectedFile.size > 2 * 1024 * 1024) {
      setError('File size must be under 2 MB');
      setFile(null);
      return;
    }

    setFile(selectedFile);
    setSuccess('File is ready to upload');
  }

  const handleSubmit = async (e) => {
    e.preventDefault();

    setSuccess('');
    setError('');

    if (!file) {
      setError('Please select a valid PDF before submitting');
      return
    }
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('fileName', file.name);
    const config = {
      headers: {
        'content-type': 'multipart/form-data',
      },
    };

    try {
      const response = await axios.post('/api/resume-upload', formData, config);

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


  return (
    <div className="file-upload">
        <form onSubmit={handleSubmit}>
          <h1>Resume File Upload</h1>

          <div className='input-container'>
            <input 
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
