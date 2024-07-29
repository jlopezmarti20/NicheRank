//Utilzied this tutorial to route each pages into each other: https://www.youtube.com/watch?v=6c2NqDyxppU&list=PLzMcBGfZo4-kCLWnGmK0jUBmGLaJxvi4j&index=3

import React, { Component } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Score from "./Score";

import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import TextField from "@material-ui/core/TextField";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import Radio from "@material-ui/core/Radio";
import RadioGroup from "@material-ui/core/RadioGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import { Typography } from "@material-ui/core";

export default class Home extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <Router>
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            height: "100vh",
            width: "100vw",
            background: "linear-gradient(to bottom, #3870E5, #5ae67f)",
            padding: "20px",
          }}
        >
          <Routes>
            <Route
              path="/"
              element={
                <Grid container spacing={1}>
                  <Grid item xs={12} align="center">
                    <Typography component="h4" variant="h4">
                      Welcome to your Niche Ranking Music
                    </Typography>
                  </Grid>
                  <Grid item xs={12} align="center">
                    <Typography component="h5" variant="h5">
                      Learn more about your music taste and compare it to others
                      with Obscurify.
                    </Typography>
                  </Grid>
                  <Grid item xs={12} align="center">
                    <Button
                      color="secondary"
                      variant="contained"
                      style={{
                        minWidth: "150px",
                        height: "150px",
                        borderRadius: "50%",
                        padding: "10px",
                        fontSize: "1.5rem",
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
      </Router>
    );
  }
}
