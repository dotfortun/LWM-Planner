import React, { useContext } from "react";
import { Col, Container, Row } from "react-bootstrap";

import { Context } from "../store/appContext";
import { Header } from "../component/header";
import { LoginForm } from "../component/login";

import "../../styles/home.css";

export const Home = () => {
  const { store, actions } = useContext(Context);

  return (
    <Container fluid>
      <Row>
        <Col xs={12}>
          <Header title="Test Header" />
        </Col>
      </Row>
      <Row>
        <Col sm={{ span: 8, offset: 2 }}></Col>
      </Row>
    </Container>
  );
};
