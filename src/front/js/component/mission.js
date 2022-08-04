import React, { useReducer, useContext, useEffect } from "react";
import { Button, Card, Col, Form, Placeholder, Row } from "react-bootstrap";

import { Context } from "../store/appContext";

const reducer = (state, action) => {
  console.log("Current state:", state);
  switch (action.type) {
    case "set_mission_state":
      console.log(state);
      return state;
    case "get_mission_name":
      if (state?.mission?.name) {
        return { name: state.mission.name };
      } else {
        return <Placeholder xs={6} size="lg" />;
      }
    default:
      throw new Error();
  }
};

export const MissionCard = ({ mission }) => {
  const { store } = useContext(Context);
  const [state, dispatch] = useReducer(reducer, {});

  useEffect(() => {
    dispatch({ type: "set_mission_state" });
  }, [mission]);

  return (
    <Card className="bg-secondary mb-3">
      <Card.Header>
        <h3>{state.name}</h3>
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
            <p>{null}</p>
          </Col>
          <Col>
            <ul className="pilot_prop_stack">
              <li>
                <strong>Participating:</strong>
              </li>
              {null}
            </ul>
          </Col>
        </Row>
      </Card.Body>
      <Card.Footer
        style={{
          display: !!store.user_token ? "block" : "none",
        }}
      >
        <Col className="d-flex justify-content-evenly">{null}</Col>
      </Card.Footer>
    </Card>
  );
};
