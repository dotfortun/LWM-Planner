import React, { useEffect, useState } from "react";
import { Button, Card, Col, Row } from "react-bootstrap";

export const MissionCard = ({ mission }) => {
  return (
    <Card className="bg-secondary mb-3" key={mission.id}>
      <Card.Header>
        <h3>
          {mission.name} - at {mission.location.name}
        </h3>
      </Card.Header>
      <Card.Body>
        <Row>
          <Col>
            <ul className="pilot_prop_stack">
              <li>
                DIFFICULTY:{" "}
                {new Array(mission.difficulty).fill(null).map((_, idx) => (
                  <i className="fa-solid fa-skull me-1" key={idx}></i>
                ))}
              </li>
            </ul>
          </Col>
          <Col>
            <ul className="pilot_prop_stack">
              <li>
                <hr />
              </li>
            </ul>
          </Col>
          <Col>
            <ul className="pilot_prop_stack">
              <li className="mb-1">
                <Button style={{ width: "100%" }}>Train Pilot</Button>
              </li>
              <li className="mb-1">
                <Button style={{ width: "100%" }}>Inventory / Store</Button>
              </li>
              <li className="mb-1">
                <Button style={{ width: "100%" }}>Edit Pilot</Button>
              </li>
            </ul>
          </Col>
        </Row>
      </Card.Body>
    </Card>
  );
};
