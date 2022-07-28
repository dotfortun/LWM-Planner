import React, { useEffect, useContext } from "react";
import { Button, Card, Col, Row } from "react-bootstrap";

import { Context } from "../store/appContext";

import "../../styles/pilots.css";

const PilotCard = ({ pilot }) => {
  return (
    <Card className="bg-secondary mb-3" key={pilot.id}>
      <Card.Header>
        <h3>
          {pilot.name} - Callsign "{pilot.callsign}"
        </h3>
      </Card.Header>
      <Card.Body>
        <Row>
          <Col>
            <ul className="pilot_prop_stack">
              <li>HULL: {pilot.hase.hull}</li>
              <li>AGILITY: {pilot.hase.agility}</li>
              <li>SYSTEMS: {pilot.hase.systems}</li>
              <li>ENGINEERING: {pilot.hase.engineering}</li>
              <li>GRIT: {pilot.grit}</li>
            </ul>
          </Col>
          <Col>
            <ul className="pilot_prop_stack">
              <li>Manna: {pilot.manna}</li>
              <li>
                <hr />
              </li>
              {pilot.frames.map((elem, idx) => (
                <li>{elem.name}</li>
              ))}
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
  const { store, actions } = useContext(Context);

  useEffect(() => {
    actions.rehydrate();
    actions.getActiveUser();
  }, []);

  return (
    <Row>
      <Col sm={{ span: 10, offset: 1 }}>
        {store.pilots?.map((elem, idx) => (
          <PilotCard pilot={elem} key={idx} />
        ))}
      </Col>
    </Row>
  );
};
