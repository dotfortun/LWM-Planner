import React, { useContext, useEffect, useState } from "react";
import { Col, Container, Placeholder, Row } from "react-bootstrap";

import { Context } from "../store/appContext";
import { Header } from "../component/header";

import "../../styles/home.css";
import { MissionCard } from "../component/mission";

export const Home = () => {
  const { store, actions } = useContext(Context);
  const [missions, setMissions] = useState([
    <MissionCard placeholder={true} key={0} />,
  ]);
  const [render, rerender] = useState(false);

  useEffect(() => {
    actions.getMissions().then(() => {
      actions.rehydrate();
      const misioncards = store.missions?.map((elem, idx) => {
        return <MissionCard mission={elem} key={idx} />;
      });
      setMissions(misioncards);
      console.log(store);
    });
  }, []);

  return (
    <Container fluid>
      <Row>
        <Col xs={12}>
          <Header title="Available Missions" />
        </Col>
      </Row>
      <Row>
        <Col sm={{ span: 8, offset: 2 }}>{missions}</Col>
      </Row>
    </Container>
  );
};
