import React, { useReducer, useContext, useEffect, useState } from "react";
import { Button, Card, Col, Form, Placeholder, Row } from "react-bootstrap";

import { Context } from "../store/appContext";

const MissionPlaceholder = () => {
  const { store } = useContext(Context);

  return (
    <Card className="bg-secondary mb-3">
      <Card.Header>
        <h3>
          <Placeholder xs={6} size="lg" />
        </h3>
        <h4>
          Location: <Placeholder xs={6} size="md" />
        </h4>
        <h6>
          DIFFICULTY: <Placeholder xs={4} size="lg" />
        </h6>
      </Card.Header>
      <Card.Body>
        <Row>
          <Col>
            <p>
              <Placeholder xs={12} size="sm" />
              <Placeholder xs={12} size="sm" />
              <Placeholder xs={12} size="sm" />
              <Placeholder xs={12} size="sm" />
            </p>
          </Col>
          <Col>
            <ul className="pilot_prop_stack">
              <li>
                <strong>Participating:</strong>
              </li>
              <li>
                <Placeholder xs={12} size="sm" />
              </li>
              <li>
                <Placeholder xs={12} size="sm" />
              </li>
              <li>
                <Placeholder xs={12} size="sm" />
              </li>
            </ul>
          </Col>
        </Row>
      </Card.Body>
    </Card>
  );
};

const Participating = ({ pilots }) => {
  return (
    <ul className="pilot_prop_stack">
      <li>
        <strong>Participating:</strong>
      </li>
      {pilots?.map((elem, idx) => (
        <li key={idx}>
          {elem.name} - <em>"{elem.callsign}"</em>
        </li>
      ))}
    </ul>
  );
};

const MissionCardButtons = ({ mission_state }) => {
  const { store } = useContext(Context);

  switch (mission_state?.value) {
    case "OPEN":
      return (
        <Col className="d-flex justify-content-evenly">
          <Form.Select style={{ width: "calc(100%/3)" }}>
            <option defaultValue={true}>Select Pilot</option>
            {store?.pilots?.map((elem, idx) => {
              return <option key={idx}>{elem.name}</option>;
            })}
          </Form.Select>
          <Button>Join Mission</Button>
        </Col>
      );
    case "PLANNING":
    case "DELAYED":
      return (
        <Col className="d-flex justify-content-evenly">
          <Button variant="danger">Leave Mission</Button>
        </Col>
      );
    default:
      return <></>;
  }
};

export const MissionCard = ({ mission }) => {
  const { store } = useContext(Context);

  useEffect(() => {
    console.log(mission);
  }, []);

  if (!mission) {
    return <MissionPlaceholder />;
  }

  return (
    <Card className="bg-secondary mb-3">
      <Card.Header>
        <h3>{mission?.name}</h3>
        <h4>Location: {mission?.location?.name}</h4>
        <h6>
          DIFFICULTY:{" "}
          {new Array(mission?.difficulty).fill(null).map((_, idx) => (
            <i className="fa-solid fa-skull me-1" key={idx}></i>
          ))}
        </h6>
      </Card.Header>
      <Card.Body>
        <Row>
          <Col>
            <p>{mission?.description}</p>
          </Col>
          <Col>
            <Participating pilots={mission?.pilots} />
          </Col>
        </Row>
      </Card.Body>
      <Card.Footer
        style={{
          display: !!store.user_token ? "block" : "none",
        }}
      >
        <MissionCardButtons mission_state={mission?.mission_state} />
      </Card.Footer>
    </Card>
  );
};
