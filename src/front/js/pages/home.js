import React, { useContext } from "react";
import { Col, Container, Row } from "react-bootstrap";

import { Context } from "../store/appContext";
import { Header } from "../component/header";
import { LoginForm } from "../component/login";

import "../../styles/home.css";
import { MissionCard } from "../component/mission";

export const Home = () => {
  const { store, actions } = useContext(Context);

  let mission = {
    description:
      "Lets shoot some doods and get some loots.  Yes, you can bring your draek.",
    difficulty: 1,
    is_job: true,
    location: {
      description: "",
      name: "Yomi Gate",
      parent: "Izanagi",
    },
    loot: [],
    mission_state: {
      name: "Open",
      value: "OPEN",
    },
    name: "Gate Camp On Yomi Gate",
    pilots: [
      {
        id: 1,
        pilot: "Test McTestington",
      },
    ],
    scheduled_date: "Sat, 06 Aug 2022 17:00:00 GMT",
  };

  return (
    <Container fluid>
      <Row>
        <Col xs={12}>
          <Header title="Available Missions" />
        </Col>
      </Row>
      <Row>
        <Col sm={{ span: 8, offset: 2 }}>
          <MissionCard mission={mission} />
        </Col>
      </Row>
    </Container>
  );
};
