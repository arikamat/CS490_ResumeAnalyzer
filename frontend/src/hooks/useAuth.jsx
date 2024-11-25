import React from 'react';
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

//custom hook created by us to deal with routing and auth
function useAuth(){
  const navigate = useNavigate();
  
  useEffect(() => {
    //get token
    const token = localStorage.getItem('token');

    if (!token) { //no token requires login :)
      navigate('/login'); 
      return;
    }

    try {
      const payload = JSON.parse(atob(token.split('.')[1])); 
      const isExpired = payload.exp * 1000 < Date.now(); //if expired remove it and then we require login again
      if (isExpired) {
        localStorage.removeItem('token'); 
        navigate('/login'); 
      }
    } catch (error) { //odd case where we have some issue with token 
      console.error('Invalid token format', error);
      navigate('/login');
    }
  }, [navigate]);
};

export default useAuth;