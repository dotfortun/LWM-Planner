import React from "react";
import "../../styles/header.css";

export const Header = ({ title }) => {
  return (
    <h1 className="lancer_red_bg text-light">
      <div>{title}</div>
    </h1>
  );
};
