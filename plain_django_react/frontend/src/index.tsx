import React from "react";
import { createRoot } from "react-dom/client";

function AppRoot() {
  return <h1>Hello world!</h1>;
}

const root = createRoot(document.getElementById("app"));
root.render(<AppRoot />);
