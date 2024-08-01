import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  useLocation,
} from "react-router-dom";
import { Grid, Typography, Button } from "@mui/material";
import Score from "./Score";

function App() {
  const location = useLocation();
  const isHomePage = location.pathname === "/";

  return (
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
        <Route
          path="/"
          element={
            <Grid container spacing={1}>
              <Grid item xs={12} align="center">
                <Typography
                  component="h4"
                  variant="h4"
                  style={{
                    fontSize: "7rem", // Increase font size for home page
                    fontWeight: "bold",
                    color: "#fff",
                  }}
                >
                  Welcome to your Niche Ranking Music
                </Typography>
              </Grid>
              <Grid item xs={12} align="center">
                <Typography
                  component="h5"
                  variant="h5"
                  style={{
                    fontSize: "6rem", // Increase font size for home page
                    color: "#fff",
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
                    minWidth: "500px",
                    height: "500px",
                    borderRadius: "50%",
                    padding: "10px",
                    fontSize: "5rem",
                  }}
                  to="/Score"
                  component={Link}
                >
                  Login
                </Button>
              </Grid>
            </Grid>
          }
        />
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
