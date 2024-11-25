import React from "react";
import { Link } from "react-router-dom";
import './Navbar.css';
import { useEffect, useState } from "react";
import isJWTValid from "../util/auth";
import { useAuth } from "../context/AuthContext";

//component for navbar and links to various 
function Navbar() {
  const {isAuth, login, logout} = useAuth();

  return (
    <nav className="navbar">
      <ul className="nav-list">
        <li className="nav-item">
          <Link to="/" className="nav-link">Home</Link>
        </li>
        {!isAuth && (
          <>
            <li className="nav-item">
              <Link to="/register" className="nav-link">Sign Up</Link>
            </li>
            <li className="nav-item">
              <Link to="/login" className="nav-link">Login</Link>
            </li>
          </>
        )}
        {isAuth && (
          <>
            <li className="nav-item">
              <Link to="/upload" className="nav-link">Resume & Job Description Upload</Link>
            </li>
            <li className="nav-item">
              <Link to="/dashboard" className="nav-link">Dashboard</Link>
            </li>
            <li className="nav-item">
              <div onClick={logout} className="nav-link">Logout</div>
            </li>
          </>
        )}

      </ul>
    </nav>
  );

}
export default Navbar;
