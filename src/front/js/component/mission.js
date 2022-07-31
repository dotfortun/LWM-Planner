import React, { useEffect, useState, useContext } from "react";
import { Button, Card, Col, Form, Placeholder, Row } from "react-bootstrap";

import { Context } from "../store/appContext";

export const MissionCard = ({ mission, placeholder }) => {
  const { store, actions } = useContext(Context);
  const [loaded, load] = useState(false);
  const [onMission, setOnMission] = useState(false);
  const [desc, setDesc] = useState(
    <>
      <Placeholder xs={12} size="md" />
      <Placeholder xs={12} size="md" />
      <Placeholder xs={12} size="md" />
    </>
  );

  useEffect(() => {
    if (typeof store.pilots == Array) {
      console.log("Ding!");
    }
  }, [store.pilots]);

  if (placeholder) {
    return (
      <Card className="bg-secondary mb-3">
        <Card.Header>
          <h3>
            <Placeholder xs={6} size="lg" />
          </h3>
          <h4>
            Location: <Placeholder xs={4} size="md" />
          </h4>
          <h6>
            DIFFICULTY: <Placeholder xs={4} size="md" />
          </h6>
        </Card.Header>
        <Card.Body>
          <Row>
            <Col>
              <p></p>
            </Col>
            <Col>
              <ul className="pilot_prop_stack">
                <li>
                  <strong>Participating:</strong>
                </li>
                <li>
                  <Placeholder xs={12} size="md" />
                </li>
                <li>
                  <Placeholder xs={12} size="md" />
                </li>
              </ul>
            </Col>
          </Row>
        </Card.Body>
        <Card.Footer>
          <Col className="d-flex justify-content-evenly">
            <Placeholder.Button xs={3} size="md" />
            <Placeholder.Button xs={3} size="md" />
          </Col>
        </Card.Footer>
      </Card>
    );
  }
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
            <p>{mission.description}</p>
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
      <Card.Footer
        style={{
          display: !!store.user_token ? "block" : "none",
        }}
      >
        <Col className="d-flex justify-content-evenly">
          {onMission ? (
            <>
              <Button>Schedule Mission</Button>{" "}
              <Button variant="danger">Leave Mission</Button>
            </>
          ) : (
            <>
              <Form.Select style={{ width: "calc(100%/3)" }}>
                <option>Select a pilot</option>
                {store.pilots?.map((elem, idx) => (
                  <option key={idx}>
                    {elem.name} "{elem.callsign}"
                  </option>
                ))}
              </Form.Select>{" "}
              <Button>Join Mission</Button>
            </>
          )}
        </Col>
      </Card.Footer>
    </Card>
  );
};
