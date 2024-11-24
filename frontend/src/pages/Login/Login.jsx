import React, { useState } from 'react';
import axios from 'axios';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [notification, setNotification] = useState('');

  const onButtonClick = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/login', { 
        email, 
        password 
      });
      if (response.status == 200) {
        localStorage.setItem('token', response.data.token); 
        setNotification("Login successful");
      } else {
        throw new Error('Login failed wrong credentials');
      }
    } catch (error) {
      setNotification(`Login failed wrong credentials`);
    }
  };

  return (
    <div className={'mainContainer'}>
      <div className={'titleContainer'}>
        <div>Login</div>
      </div>
      <br />
      <form onSubmit={onButtonClick}>
        <div className={'inputContainer'}>
          <input
            type="email"
            value={email}
            placeholder="Email"
            onChange={(ev) => setEmail(ev.target.value)}
            className={'inputBox'}
            required
          />
        </div>
        <br />
        <div className={'inputContainer'}>
          <input
            type="password"
            value={password}
            placeholder="Password"
            onChange={(ev) => setPassword(ev.target.value)}
            className={'inputBox'}
            required
          />
        </div>
        <br />
        <div className={'inputContainer'}>
          <input
            className={'inputButton'}
            type="submit"
            value="Log in"
          />
        </div>
      </form>
      <p>{notification}</p>
    </div>
  );
};

export default Login;
