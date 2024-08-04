import React, { Component } from "react";
import { Grid, Typography, Box, Button } from "@material-ui/core";
import { Link } from "react-router-dom";

export default class Score extends Component {
  constructor(props) {
    super(props);
    this.state = {
      artists: [],
      songs: [],
      obscurityScore: 0,
      error: null,
    };
  }

  componentDidMount() {
    fetch("http://127.0.0.1:5000/user_metrics")
      .then((response) => response.json())
      .then((data) => {
        this.setState({
          artists: data.topArtists,
          songs: data.topSongs,
          obscurityScore: (data.pop_score * 100).toFixed(1),
        });
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        this.setState({ error: error.message });
      });
  }

  render() {
    const { artists, songs, obscurityScore, error } = this.state;

    return (
      <div
        style={{
          height: "100vh",
          background: "#AD96DC",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontFamily: "'Roboto', sans-serif",
        }}
      >
        <Button
          color="primary"
          variant="contained"
          to="/"
          component={Link}
          style={{
            fontSize: "1.5rem",
            padding: "12px 24px",
            position: "absolute",
            top: "10px",
            left: "10px",
          }}
        >
          Back
        </Button>
        <Grid container spacing={6} style={{ height: "100%", width: "auto" }}>
          <Grid
            item
            xs={12}
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              position: "relative",
            }}
          >
            <Typography
              component="h4"
              variant="h4"
              align="center"
              style={{
                position: "absolute",
                top: 150,
                left: -690,
                whiteSpace: "nowrap",
                color: "white",
                fontFamily: "'Roboto', sans-serif",
                fontWeight: "bold",
                borderBottom: "10px solid white",
                paddingBottom: "10px",
                fontSize: "2.5rem",
              }}
            >
              Your top Artist playlist
            </Typography>
            <Typography
              component="h4"
              variant="h4"
              align="center"
              style={{
                position: "absolute",
                top: 150,
                left: -220,
                whiteSpace: "nowrap",
                color: "white",
                fontFamily: "'Roboto', sans-serif",
                fontWeight: "bold",
                borderBottom: "10px solid white",
                paddingBottom: "10px",
                fontSize: "2.5rem",
              }}
            >
              Your top Song playlist
            </Typography>
            <Typography
              component="h4"
              variant="h4"
              align="center"
              style={{
                marginLeft: "20px",
                whiteSpace: "nowrap",
                background: "#AD96DC",
                padding: "20px",
                borderRadius: "10px",
                boxShadow: "10px 10px 10px rgba(0, 0, 0, 0.1)",
                position: "absolute",
                top: 0,
                left: 230,
                color: "white",
                fontFamily: "'Roboto', sans-serif",
                fontWeight: "bold",
                fontSize: "2.5rem",
              }}
            >
              Obscurity Score: {obscurityScore}%
            </Typography>
          </Grid>
          <Grid
            container
            item
            xs={12}
            spacing={3}
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              marginTop: "400px",
              position: "absolute",
              top: -175,
              left: -50,
            }}
          >
            <Grid item xs={6} style={{ padding: "20px" }}>
              <Grid container direction="column" spacing={2}>
                {artists.map((artist, index) => (
                  <Box
                    key={index}
                    style={{
                      backgroundColor: "rgba(223,214,239, 0.3)",
                      padding: "20px",
                      marginBottom: "20px",
                      textAlign: "left",
                      fontSize: "2.5rem",
                      color: "white",
                      fontWeight: "bold",
                      whiteSpace: "nowrap",
                      borderRadius: "5px",
                      boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)",
                      width: "400px",
                      height: "45px",
                      position: "relative",
                      left: "50px",
                    }}
                  >
                    {index + 1} / {artist}
                  </Box>
                ))}
              </Grid>
            </Grid>
            <Grid item xs={6} style={{ padding: "20px" }}>
              <Grid container direction="column" spacing={2}>
                {songs.map((song, index) => (
                  <Box
                    key={index}
                    style={{
                      backgroundColor: "rgba(223,214,239, 0.3)",
                      padding: "20px",
                      marginBottom: "20px",
                      textAlign: "left",
                      fontSize: "2.5rem",
                      color: "white",
                      fontWeight: "bold",
                      whiteSpace: "nowrap",
                      borderRadius: "5px",
                      boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)",
                      width: "870px",
                      height: "45px",
                      position: "relative",
                      left: "-175px",
                    }}
                  >
                    {index + 1} / {song}
                  </Box>
                ))}
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </div>
    );
  }
}
