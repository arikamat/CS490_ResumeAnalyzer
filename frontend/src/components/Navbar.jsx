import { Link } from "react-router-dom";
import './Navbar.css'; 

//component for navbar and links to various 
function Navbar() {
  return (
    <nav className="navbar">
      <ul className="nav-list">
        <li className="nav-item">
          <Link to="/" className="nav-link">Home</Link>
        </li>
        <li className="nav-item">
          <Link to="/login" className="nav-link">Login</Link>
        </li>
        <li className="nav-item">
          <Link to="/register" className="nav-link">Sign Up</Link>
        </li>
        <li className="nav-item">
          <Link to="/dashboard" className="nav-link">Dashboard</Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
