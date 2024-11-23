import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import SignUp from './components/SignUp.jsx'; 
import Login  from './components/Login.jsx';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <SignUp/> 
  </StrictMode>
);
