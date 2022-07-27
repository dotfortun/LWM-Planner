import React, { useEffect, useState } from "react";

export const Footer = () => {
  const [message, setMessage] = useState("");

  useEffect(() => {
    let messages = [
      "The GSV Ominous Doorstop would like you to know you are irreplaceable. For now.",
    ];

    setMessage(messages[Math.floor(Math.random() * messages.length)]);
  }, []);

  return (
    <footer className="footer mt-auto py-3 text-center">
      <p>{message}</p>
    </footer>
  );
};
