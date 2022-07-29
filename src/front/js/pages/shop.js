import React, { useContext, useEffect, useRef } from "react";
import { Col, Container, Row, Button, Card } from "react-bootstrap";

import { Context } from "../store/appContext";
import { Header } from "../component/header";

import "../../styles/shop.css";

const ShopCard = ({ item }) => {
  return (
    <Card className="bg-secondary mb-3" key={item.id}>
      <Card.Header className="d-flex justify-content-between">
        <h3>{item.name}</h3>
        <Button>Purchase Item</Button>
      </Card.Header>
      <Card.Body>
        <Row>
          <p>{item.description}</p>
        </Row>
      </Card.Body>
    </Card>
  );
};

export const ShopPage = () => {
  const { store, actions } = useContext(Context);
  const pass = useRef(null);

  useEffect(() => {
    actions.rehydrate();
    actions.getShop();
  }, []);

  return (
    <Container fluid>
      <Row>
        <Col xs={{ span: 10, offset: 1 }}>
          <Header title={`Frames:`} />
          {store.shop?.frame?.map((elem, idx) => (
            <ShopCard item={elem} key={idx} />
          ))}
        </Col>
      </Row>
      <Row>
        <Col xs={{ span: 10, offset: 1 }}>
          <Header title={`Weapons:`} />
          {store.shop?.weapon?.map((elem, idx) => (
            <ShopCard item={elem} key={idx} />
          ))}
        </Col>
      </Row>
      <Row>
        <Col xs={{ span: 10, offset: 1 }}>
          <Header title={`Systems:`} />
          {store.shop?.system?.map((elem, idx) => (
            <ShopCard item={elem} key={idx} />
          ))}
        </Col>
      </Row>
      <Row>
        <Col xs={{ span: 10, offset: 1 }}>
          <Header title={`Mods:`} />
          {store.shop?.mod?.map((elem, idx) => (
            <ShopCard item={elem} key={idx} />
          ))}
        </Col>
      </Row>
    </Container>
  );
};
