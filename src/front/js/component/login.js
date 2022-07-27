import React, { useRef, useContext } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { useNavigate } from "react-router-dom";

import { Context } from "../store/appContext";

export const LoginForm = () => {
  const navigate = useNavigate();
  const { store, actions } = useContext(Context);
  const email = useRef(null);
  const pass = useRef(null);

  const handleForm = () => {
    actions
      .login(email?.current?.value, pass?.current?.value)
      .then(() => navigate("/test"))
      .catch(() => handleFailedLogin());
  };

  const handleFailedLogin = () => {
    return;
  };

  return (
    <>
      <Form.Group className="mb-3">
        <Form.Control type="email" placeholder="Enter email" ref={email} />
        <Form.Text className="text-muted">
          We'll never share your email with anyone else.
        </Form.Text>
      </Form.Group>
      <Form.Group className="mb-3">
        <Form.Control type="password" placeholder="Password" ref={pass} />
      </Form.Group>

      <Button variant="primary" onClick={handleForm}>
        Log In
      </Button>
    </>
  );
};
