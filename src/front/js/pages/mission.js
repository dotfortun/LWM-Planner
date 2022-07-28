import React from "react";
import { Col, Container, Row, Button, Form } from "react-bootstrap";
import { useParams } from "react-router-dom";

import { Header } from "../component/header";

export const MissionPage = () => {
  const { id } = useParams();

  return (
    <Row>
      <Col xs={12}>
        <Header title={id} />
      </Col>
    </Row>
  );
};
