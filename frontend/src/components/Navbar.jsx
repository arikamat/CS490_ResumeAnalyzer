import { Link } from 'react-router-dom';
function Navbar() {
  return (
    <nav>
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/login" >Login</Link></li>
        <li ><Link to="/register">Sign Up</Link></li>
      </ul>
    </nav>
  );
}



export default Navbar;
