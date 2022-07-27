import React from "react";
import { Button, Card, Col, Row } from "react-bootstrap";

import "../../styles/pilots.css";

const PilotCard = ({ pilot }) => {
  return (
    <Card className="bg-secondary" key={pilot.id}>
      <Card.Header>
        <h3>
          {pilot.name} - Callsign "{pilot.callsign}"
        </h3>
      </Card.Header>
      <Card.Body>
        <Row>
          <Col>
            <ul className="pilot_prop_stack">
              <li>HULL: {pilot.hull}</li>
              <li>AGILITY: {pilot.agility}</li>
              <li>SYSTEMS: {pilot.sytstems}</li>
              <li>ENGINEERING: {pilot.engineering}</li>
              <li>GRIT: {pilot.grit}</li>
            </ul>
          </Col>
          <Col>
            <ul className="pilot_prop_stack">
              <li>Manna: {pilot.manna}</li>
              <li>
                <hr />
              </li>
              <li>
                IPS-N DRAKE <em>"CAN I HAS DRAEK"</em>
              </li>
              <li>
                GMS EVEREST <em>"CHEEPFLEET"</em>
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

export const PilotPage = () => {
  return (
    <Row>
      <Col sm={{ span: 10, offset: 1 }}>
        <PilotCard pilot={} />
      </Col>
    </Row>
  );
};
