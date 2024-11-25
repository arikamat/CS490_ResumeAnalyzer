import React, { useState } from 'react';
import axios from 'axios';
import '../../assets/Global.css';
import Loading from '../../components/Loading'
// Handles functionality of login page with email and password
const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [notification, setNotification] = useState('');
  const [loading, setLoading] = useState(false);

  // Function that handles button click and sends the Login data to server
  const onButtonClick = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/login', {
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
    setLoading(false);
  };

  //Format of the page
  return (
    <>
      {loading ? (
        <Loading />
      )
        :
        (<div className={'mainContainer'}>
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
                value="Sign in"
              />
            </div>
          </form>
          <p>{notification}</p>
        </div>)}
    </>
  );
};

export default Login;
