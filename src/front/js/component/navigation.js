import React, { useContext } from "react";
import { Navbar, Nav, NavDropdown, Container } from "react-bootstrap";
import { useLocation } from "react-router-dom";

import { LoginForm } from "./login";
import { Context } from "../store/appContext";

export const Navigation = () => {
  const { store } = useContext(Context);
  const loc = useLocation();

  return (
    <Navbar bg="dark" variant="dark">
      <Container>
        <Navbar.Brand href="/">
          <i className="fas fa-lg fa-torii-gate"></i> &nbsp; LWM Planner
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav" className="justify-content-end">
          <Nav>
            <Nav.Link href="/">Home</Nav.Link>
            {!!store.user_token ? (
              <NavDropdown
                title="Account"
                href="/profile"
                menuVariant="dark"
                align="end"
              >
                <NavDropdown.Item href="/profile">
                  <span>Profile</span>
                </NavDropdown.Item>
                <NavDropdown.Item href="/profile/pilots">
                  <span>Pilots</span>
                </NavDropdown.Item>
              </NavDropdown>
            ) : null}
            <NavDropdown
              title="Login"
              menuVariant="dark"
              align="end"
              autoClose="outside"
            >
              <NavDropdown.Item>
                <LoginForm nav_to={loc} />
              </NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};
