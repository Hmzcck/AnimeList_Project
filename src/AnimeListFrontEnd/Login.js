import React, { useState } from 'react';
import axios from 'axios'; // Import axios for making HTTP requests
import './Login.css'; // Import the CSS file
import { useNavigate, Link } from 'react-router-dom';
import { getUserId, setUserId } from './userToken';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const navigate = useNavigate();

  const handleChange = (event) => {
    const { name, value } = event.target;
    if (name === 'username') {
      setUsername(value);
    } else if (name === 'password') {
      setPassword(value);
    }
    setErrorMessage('');
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!username || !password) {
      setErrorMessage('Username and password are required.');
      return;
    }

    try {
      // Make an HTTP POST request using Axios
      const response = await axios.post('/api/users/login', { username, password });

      // Handle the response, e.g., update state or redirect to another page
      if (response.status === 200) {
        console.log(response.data);
        setUserId(Number(response.data[0]));
        if(response.data[1] === 'user')
            navigate('/HomePage');
        else if(response.data[1] === 'admin')
            navigate('/admin');
      } else {
        console.error('Login failed:');
      }
    } catch (error) {
      // Handle errors, e.g., display an error message to the user
      console.error('Login failed:', error.message);
    }
  };

  return (
    <div className="container">
      <img src="https://variety.com/wp-content/uploads/2023/04/Demon-Slayer-Swordsmith-Village-Arc-Stills-4-res.jpg?w=1000" alt="Login Image" className="loginImage" />
      <form className="form" onSubmit={handleSubmit}>
        <label>
          <input
            placeholder="Username"
            name="username"
            value={username}
            onChange={handleChange}
            className="inputField"
          />
        </label>
        <br />
        <label>
          <input
            placeholder="Password"
            name="password"
            value={password}
            onChange={handleChange}
            className="inputField"
          />
        </label>
        <br />
        <button type="submit" className="loginButton">
          Log In
        </button>
        {errorMessage && <p className="errorMessage">{errorMessage}</p>}

        <p className="registerMessage">
          Don't have an account, click Register button!
        </p>
        <Link to="/register">
          <button type="button" className="registerButton">
            Register
          </button>
        </Link>
      </form>
    </div>
  );
};

export default Login;
