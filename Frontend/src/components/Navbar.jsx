import { NavLink } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
      <div className="container">
        <NavLink className="navbar-brand fw-bold" to="/">
          AI Support Ticket Classifier
        </NavLink>
      </div>
    </nav>
  );
}

export default Navbar;
