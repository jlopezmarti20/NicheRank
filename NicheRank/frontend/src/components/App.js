import React, { Component } from "react";
import { render } from "react-dom";
import Home from "./Home";
import Score from "./Score";

// Main React component that serves as the entry point of our application
export default class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <Home /> // Render the Home component inside the App component
      </div>
    );
  }
}

const appDiv = document.getElementById("app");

render(<App />, appDiv); // Effectively start our application
