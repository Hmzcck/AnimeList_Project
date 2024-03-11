// src/App.js
import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from './429Project/Login';
import Register from './429Project/Register';
import HomePage from './429Project/HomePage';
import Content from './Content';
import Admin from './429Project/admin';
import AddAnime from './429Project/adminaddanime';
import RemoveAnime from './429Project/removeAnime';



function App() {
  return (
    <BrowserRouter>
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/Register" element={<Register />} />
      <Route path="/HomePage" element={<HomePage />} />
      <Route path="/Content" element={<Content />} />
      <Route path="/admin" element={<Admin />} />
      <Route path="/addanime" element={<AddAnime />} />
      <Route path="/removeAnime" element={<RemoveAnime />} />
    </Routes>
    </BrowserRouter>
  );
}

export default App; 


// src/App.js
/*import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import Login from './429Project/Login';
import SignUp from './429Project/SignUp';
import HomePage from './429Project/HomePage';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    // Assuming successful login logic here
    setIsLoggedIn(true);
  };

  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <Switch>
            <Route path="/login">
              {isLoggedIn ? <Redirect to="/main" /> : <Login onLogin={handleLogin} />}
            </Route>
            <Route path="/signup" component={SignUp} />
            <Route path="/main">
              {isLoggedIn ? <HomePage /> : <Redirect to="/login" />}
            </Route>
            <Redirect from="/" to="/login" />
          </Switch>
        </header>
      </div>
    </Router>
  );
}

export default App;*/
