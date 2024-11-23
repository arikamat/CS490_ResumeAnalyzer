import React, { useState } from 'react';
import axios from 'axios';

const SignUp = () => {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [notification, setNotification] = useState('');

  const onButtonClick = async (e) => {
    e.preventDefault();
    
    if (password !== confirmPassword) {
      setNotification("Passwords do not match");
      return;
    }

    try {
      const response = await axios.post('/api/signup', {
        email,
        username,
        password,
      });
      localStorage.setItem('token', response.data.token); 
      setNotification("Signup completed");
    } catch (error) {
      setNotification("Signup failed", error);
    }
  };

  return (
    <div className={'mainContainer'}>
      <div className={'titleContainer'}>
        <div>Sign Up</div>
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
            type="text"
            value={username}
            placeholder="Username"
            onChange={(ev) => setUsername(ev.target.value)}
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
            type="password"
            value={confirmPassword}
            placeholder="Confirm Password"
            onChange={(ev) => setConfirmPassword(ev.target.value)}
            className={'inputBox'}
            required
          />
        </div>
        <br />
        <div className={'inputContainer'}>
          <input
            className={'inputButton'}
            type="submit"
            value="Sign Up"
          />
        </div>
      </form>
      <p>{notification}</p>
    </div>
  );
};

export default SignUp;
