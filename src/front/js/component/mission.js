import React, { useEffect, useState } from "react";
import { Button, Card, Col, Row } from "react-bootstrap";

export const MissionCard = ({ mission }) => {
  return (
    <Card className="bg-secondary mb-3" key={mission.id}>
      <Card.Header>
        <h3>{mission.name}</h3>
        <h4>Location: {mission.location.name}</h4>
        <h6>
          DIFFICULTY:{" "}
          {new Array(mission.difficulty).fill(null).map((_, idx) => (
            <i className="fa-solid fa-skull me-1" key={idx}></i>
          ))}
        </h6>
      </Card.Header>
      <Card.Body>
        <Row>
          <Col>
            <ul className="pilot_prop_stack">
              <li>{mission.description}</li>
              <li>
                <hr />
              </li>
              <li></li>
            </ul>
          </Col>
          <Col>
            <ul className="pilot_prop_stack">
              <li>
                <strong>Participating:</strong>
              </li>
              {mission.pilots.map((elem, idx) => (
                <li key={idx}>{elem.pilot}</li>
              ))}
              <li>
                <hr />
              </li>
            </ul>
          </Col>
          <Col>
            <ul className="pilot_prop_stack">
              <li className="mb-1">
                <Button style={{ width: "100%" }}>Join Mission</Button>
              </li>
              <li className="mb-1">
                <Button style={{ width: "100%" }}>Schedule Mission</Button>
              </li>
              <li className="mb-1">
                <Button variant="danger" style={{ width: "100%" }}>
                  Leave Mission
                </Button>
              </li>
            </ul>
          </Col>
        </Row>
      </Card.Body>
    </Card>
  );
};
