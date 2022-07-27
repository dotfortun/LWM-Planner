import React, { useState, useEffect } from "react";
import "../../styles/header.css";

export const Header = ({ title, size, right }) => {
  const [htmlClasses, setHtmlClasses] = useState(
    `header_root lancer_red_bg text-light my-3`
  );

  useEffect(() => {
    if (right) {
      setHtmlClasses(`header_root lancer_red_bg text-light my-3 right`);
    }
  });

  switch (size) {
    case "h1":
      return (
        <h1 className={htmlClasses}>
          <div>{title}</div>
        </h1>
      );
      break;
    case "h2":
      return (
        <h2 className={htmlClasses}>
          <div>{title}</div>
        </h2>
      );
    case "h3":
      return (
        <h3 className={htmlClasses}>
          <div>{title}</div>
        </h3>
      );
      break;
    case "h4":
      return (
        <h4 className={htmlClasses}>
          <div>{title}</div>
        </h4>
      );
      break;
    case "h5":
      return (
        <h5 className={htmlClasses}>
          <div>{title}</div>
        </h5>
      );
      break;
    case "h6":
      return (
        <h6 className={htmlClasses}>
          <div>{title}</div>
        </h6>
      );
      break;
    default:
      return (
        <h1 className={htmlClasses}>
          <div>{title}</div>
        </h1>
      );
  }
};
