import React, { useContext, useEffect, useRef } from "react";
import { Col, Container, Row, Button, Form } from "react-bootstrap";

import { Context } from "../store/appContext";
import { Header } from "../component/header";

import "../../styles/home.css";

export const ProfilePage = () => {
  const { store, actions } = useContext(Context);
  const pass = useRef(null);

  useEffect(() => {
    actions.rehydrate();
    actions.getActiveUser();
  }, []);

  const handleUpdateUser = () => {
    actions.updateActiveUser({
      password: pass.current.value,
    });
  };

  return (
    <Container fluid>
      <Row>
        <Col xs={12}>
          <Header title={`Profile: ${store.user?.email}`} />
        </Col>
      </Row>
      <Row>
        <Col xs={{ span: 4, offset: 1 }}>
          <Header title={`Password`} size="h4" />
          <Form.Group className="d-inline-flex">
            <Form.Control
              type="password"
              placeholder="Change Password"
              ref={pass}
            />
            <Button className="ms-2" onClick={handleUpdateUser}>
              Change Password
            </Button>
          </Form.Group>
        </Col>
      </Row>
    </Container>
  );
};
