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
    description: "Yes, you can bring your draek.",
    difficulty: 5,
    is_job: false,
    location: {
      description: "",
      name: "Yomi Gate",
      parent: "Izanagi",
    },
    loot: [
      {
        id: 1,
        name: "IPS-N DRAKE",
      },
    ],
    mission_state: {
      name: "Open",
      value: "OPEN",
    },
    name: "Camp Yomi Gate",
    pilots: [
      {
        callsign: "Testy",
        grit: 5,
        hase: {
          agility: 2,
          engineering: 4,
          hull: 1,
          systems: 3,
        },
        id: 1,
        manna: 1000,
        name: "Test McTestington",
      },
      {
        callsign: "Neophyte",
        grit: 2,
        hase: {
          agility: 2,
          engineering: 0,
          hull: 2,
          systems: 0,
        },
        id: 2,
        manna: 1000,
        name: "New Pilot",
      },
    ],
    scheduled_date: "Fri, 29 Jul 2022 00:00:00 GMT",
  };

  return (
    <Container fluid>
      <Row>
        <Col xs={12}>
          <Header title="Test Header" />
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
