import React from "react";
import {
  BrowserRouter as Router, // BrowserRouter for handling routing
  Routes, // Routes component to define route paths
  Route, // Route component to define individual routes
  Link, // Link component for navigation
  useLocation, // Hook to access the current location
} from "react-router-dom";
import { Grid, Typography, Button } from "@mui/material"; // Importing Material-UI components
import Score from "./Score"; // Importing the Score component

function App() {
  const location = useLocation(); // Hook to get the current location
  const isHomePage = location.pathname === "/"; // Check if the current path is the home page

  const handleLogin = () => {
    window.location.href = "http://127.0.0.1:5000/"; // Redirect to Flask backend for authentication
  };

  return (
    // Main container that sets the layout, centering, background color, and padding based on the current page
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        width: "100vw",
        background: isHomePage
          ? "linear-gradient(to bottom, #3870E5, #5ae67f)"
          : "#AD96DC",
        padding: "20px",
      }}
    >
      <Routes>
        {/* Route for the home page */}
        <Route
          path="/"
          element={
            <Grid container spacing={1}>
              <Grid item xs={12} align="center">
                <Typography
                  component="h4"
                  variant="h4"
                  style={{
                    fontSize: "2.5rem",
                    fontWeight: "bold",
                    position: "relative",
                    top: -100,
                    color: "#fff",
                  }}
                >
                  Welcome to your Niche Ranking Music!
                </Typography>
              </Grid>
              <Grid item xs={12} align="center">
                <Typography
                  component="h6"
                  variant="h6"
                  style={{
                    fontSize: "2rem",
                    color: "#fff",
                    position: "relative",
                    top: -90,
                  }}
                >
                  Learn more about your music taste and compare it to others
                  with Obscurify.
                </Typography>
              </Grid>
              <Grid item xs={12} align="center">
                <Button
                  color="secondary"
                  variant="contained"
                  style={{
                    minWidth: "200px",
                    height: "200px",
                    borderRadius: "50%",
                    padding: "10px",
                    fontSize: "2rem",
                  }}
                  onClick={handleLogin} // on click go to spotify auth
                >
                  Login
                </Button>
              </Grid>
            </Grid>
          }
        />
        {/* Route for the Score page */}
        <Route path="/Score" element={<Score />} />
      </Routes>
    </div>
  );
}

export default function Root() {
  return (
    <Router>
      <App />
    </Router>
  );
}
