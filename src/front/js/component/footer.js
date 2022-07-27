import React, { useEffect, useState } from "react";

export const Footer = () => {
  const [message, setMessage] = useState("");

  useEffect(() => {
    let messages = [
      "The GSV Ominous Doorstop would like you to know you are irreplaceable. For now.",
      "The GSV Ominous Doorstop is thankful for all of your fleshy help.",
      "01010000 01010010 01000001 01001001 01010011 01000101 00100000 01010010 01000001 00100001",
    ];

    setMessage(messages[Math.floor(Math.random() * messages.length)]);
  }, []);

  return (
    <footer className="footer mt-auto py-3 text-center">
      <small>{message}</small>
    </footer>
  );
};
