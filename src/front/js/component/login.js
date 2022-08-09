import React, { useRef, useContext, useState } from "react";
import { Button, Form, Alert } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

import { Context } from "../store/appContext";

export const LoginForm = ({ nav_to }) => {
  const navigate = useNavigate();
  const { store, actions } = useContext(Context);
  const [alert, showAlert] = useState(false);
  const email = useRef(null);
  const pass = useRef(null);

  const handleForm = () => {
    actions
      .login(email.current.value, pass.current.value)
      .then(() => {
        store.getActiveUser().then(() => {
          store.getActivePilots().then(() => {
            if (nav_to) {
              navigate(nav_to);
            } else {
              navigate(-1);
            }
          });
        });
      })
      .catch(() => showAlert(true));
  };

  const toggleAlert = () => {
    showAlert(!alert);
  };

  return (
    <Form onSubmit={handleForm}>
      <Form.Group className="mb-3">
        <Form.Control type="email" placeholder="Enter email" ref={email} />
        <Form.Text className="text-muted">
          We'll never share your email with anyone else.
        </Form.Text>
      </Form.Group>
      <Form.Group className="mb-3">
        <Form.Control type="password" placeholder="Password" ref={pass} />
      </Form.Group>
      {alert ? (
        <Alert variant="danger" onClose={toggleAlert} dismissible>
          Invalid Credentials.
        </Alert>
      ) : null}

      <Button variant="primary" onClick={handleForm}>
        Log In
      </Button>
    </Form>
  );
};
