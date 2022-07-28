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
          <div className="d-flex" style={{ height: "2.5rem" }}>
            <Form.Control type="password" placeholder="Submit" ref={pass} />
            <Button className="ms-2" onClick={handleUpdateUser}>
              Submit
            </Button>
          </div>
        </Col>
      </Row>
    </Container>
  );
};
