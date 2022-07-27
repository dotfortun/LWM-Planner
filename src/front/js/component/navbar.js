import React from "react";
import { Link } from "react-router-dom";

export const Navbar = () => {
  return (
    <nav className="navbar navbar-dark bg-dark text-light my-2">
      <div className="container">
        <Link to="/">
          <span className="navbar-brand mb-0 h1">
            <i className="fas fa-lg fa-torii-gate"></i>
          </span>
        </Link>
        <div className="ml-auto"></div>
      </div>
    </nav>
  );
};
