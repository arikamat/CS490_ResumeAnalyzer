import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import SignUp from './pages/SignUp/SignUp.jsx';
import Login from './pages/Login/Login.jsx';
import Home from './pages/Home/Home.jsx';
import Navbar from './components/Navbar.jsx';
import Upload from './pages/Upload/Upload.jsx';
const App = () => {
  return (
    <Router> 
        <Navbar/>
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login/>} />
            <Route path="/register" element={<SignUp />} />
            <Route path="/upload" element = {<Upload/>}/>

        </Routes>
    </Router>
  );
};

export default App;
