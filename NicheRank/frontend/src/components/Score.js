import React, { Component } from "react";
import { Grid, Typography, Box, Button } from "@material-ui/core";
import { Link } from "react-router-dom"; // use to route the button between the links

export default class Score extends Component {
  constructor(props) {
    super(props);
    this.state = {
      artists: [], // Holds the list of top artists
      songs: [], // Holds the list of top songs
      popularityScore: 0, // Holds the obscurity score
      error: null, // Holds any error message
    };
  }

  // Fetches user metrics from the backend when the component mounts
  componentDidMount() {
    fetch("http://127.0.0.1:5000/user_metrics")
      .then((response) => response.json())
      .then((data) => {
        this.setState({
          artists: data.topArtists, // Set the top artists
          songs: data.topSongs, // Set the top songs
          popularityScore: (data.pop_score * 100).toFixed(1), // Calculate and set the obscurity score
        });
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        this.setState({ error: error.message });
      });
  }

  render() {
    const { artists, songs, popularityScore, error } = this.state;

    return (
      <div
        // Main container that sets the full viewport height, background color, centers its children components, and applies a css specific font
        style={{
          height: "100vh",
          background: "#AD96DC",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontFamily: "'Roboto', sans-serif",
        }}
      >
        {/* Back button to navigate to the home page  and apply CSS style*/}
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
        {/* Main grid container */}
        <Grid container spacing={6} style={{ height: "100%", width: "auto" }}>
          {/* Grid item for the headers */}
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
            {/* Header for top artist playlist */}
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

            {/* Header for top song playlist */}
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

            {/* Obscurity score display */}
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
                left: 200,
                color: "white",
                fontFamily: "'Roboto', sans-serif",
                fontWeight: "bold",
                fontSize: "2.5rem",
              }}
            >
              Popularity Score: {popularityScore}%
            </Typography>
          </Grid>
          {/* Grid container for the lists */}
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
            {/* Grid item for the top artists list */}
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
            {/* Grid item for the top songs list */}
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
