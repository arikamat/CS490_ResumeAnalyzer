import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import FileUpload from './components/FileUpload.jsx'
import JobDescription from './components/JobDescription.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <FileUpload/>
    <JobDescription/>
  </StrictMode>,
)
