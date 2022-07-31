import React, { useEffect, useState } from "react";
import { Button, Card, Col, Row } from "react-bootstrap";

export const MissionCard = ({ mission }) => {
  return (
    <Card className="bg-secondary mb-3">
      <Card.Header>
        <h3>{mission.name}</h3>
        <h4>Location: {mission.location.name}</h4>
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
            <ul className="pilot_prop_stack">
              <li>{mission.description}</li>
            </ul>
          </Col>
          <Col>
            <ul className="pilot_prop_stack">
              <li>
                <strong>Participating:</strong>
              </li>
              {mission.pilots.map((elem, idx) => (
                <li key={idx}>
                  {elem.name} "{elem.callsign}"
                </li>
              ))}
            </ul>
          </Col>
        </Row>
      </Card.Body>
      <Card.Footer>
        <Col className="d-flex justify-content-evenly">
          <Button>Join Mission</Button>
          <Button>Schedule Mission</Button>
          <Button variant="danger">Leave Mission</Button>
        </Col>
      </Card.Footer>
    </Card>
  );
};
