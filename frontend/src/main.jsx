import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import SignUp from './pages/SignUp/SignUp.jsx'; 
import Login  from './pages/Login/Login.jsx';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <SignUp/>
  </StrictMode>
);
