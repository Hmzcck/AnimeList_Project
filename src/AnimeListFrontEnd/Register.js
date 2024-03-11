import React, { useState } from 'react';
import axios from 'axios';
import './Register.css';
import { useNavigate } from 'react-router-dom';

const Register = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    passwordConfirm: '',
  });
  const navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState('');

  const handleChange = (event) => {
    setFormData({ ...formData, [event.target.name]: event.target.value });
    setErrorMessage('');
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const { username, password, passwordConfirm } = formData;

    if (!username || !password || !passwordConfirm) {
      setErrorMessage('All fields are required.');
      return;
    }

    if (password !== passwordConfirm) {
      setErrorMessage('Passwords do not match.');
      return;
    }

    try {
      // Make an HTTP POST request using Axios
      const response = await axios.post('/api/users/register', { username, password, passwordConfirm });

      // Handle the response, e.g., update state or redirect to another page
      if (response.status === 200) {
        setTimeout(() => {
          navigate('/');
        }, 1000);
      }
      
      // Add navigation or further state updates if needed
    } catch (error) {
      // Handle errors, e.g., display an error message to the user
      setErrorMessage('Registration failed. Please try again.');
    }
  };

  return (
    <div className="container">
      <form className="form" onSubmit={handleSubmit}>
        <label>
          <input
            placeholder="Username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            className="inputField"
          />
        </label>
        <br />
        <label>
          <input
            placeholder="Password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            className="inputField"
          />
        </label>
        <br />
        <label>
          <input
            placeholder="PasswordConfirm"
            name="passwordConfirm"
            value={formData.passwordConfirm}
            onChange={handleChange}
            className="inputField"
          />
        </label>
        <br />
        <button type="submit" className="loginButton">
          Register
        </button>
        {errorMessage && <p className="errorMessage">{errorMessage}</p>}
      </form>
    </div>
  );
};

export default Register;
