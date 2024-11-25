import React, { useState } from 'react';
import axios from 'axios';
import '../../assets/Global.css';
import Loading from '../../components/Loading'

// Handles functionality of login page with email, username, password, confirmpassword
const SignUp = () => {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [notification, setNotification] = useState('');
  const [loading, setLoading] = useState(false);

  // Function that handles button click and sends the SignUp data to server if valid
  const onButtonClick = async (e) => {
    e.preventDefault();
    

    if (password !== confirmPassword) {
      setNotification("Passwords do not match");
      return;
    }
    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/register', {
        email,
        username,
        password,
      });

      if (response.status == 201) {
        setNotification("Signup completed");
      } else {
        throw new Error('Signup failed email is not unique');
      }
    } catch (error) {
      setNotification(`Signup failed email is not unique`);
    }
    setLoading(false);

  };

  // Format of the page
  return (
    <>
      {loading ? (<Loading />) : (<div className={'mainContainer'}>
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
      </div>)}
    </>
  );
};

export default SignUp;
