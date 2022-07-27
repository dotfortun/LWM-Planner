import React from "react";
import { Button, Card, Col, Row } from "react-bootstrap";

import "../../styles/pilots.css";

export const PilotPage = () => {
  return (
    <Row>
      <Col sm={{ span: 10, offset: 1 }}>
        <Card className="bg-secondary">
          <Card.Header>
            <h3>Test McTestington - Callsign "Testy"</h3>
          </Card.Header>
          <Card.Body>
            <Row>
              <Col>
                <ul className="pilot_prop_stack">
                  <li>HULL: 1</li>
                  <li>AGILITY: 2</li>
                  <li>SYSTEMS: 3</li>
                  <li>ENGINEERING: 4</li>
                  <li>GRIT: 5</li>
                </ul>
              </Col>
              <Col>
                <ul className="pilot_prop_stack">
                  <li>Manna: 1000</li>
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
      </Col>
    </Row>
  );
};
