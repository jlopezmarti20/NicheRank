import React, { Component } from "react";
import { Grid, Typography, Box, Button } from "@material-ui/core";
import { Link } from "react-router-dom";

export default class Score extends Component {
  constructor(props) {
    super(props);
    this.state = {
      user: "Jesus",
      playlist: [
        "Song 1",
        "Song 2",
        "Song 3",
        "Song 4",
        "Song 5",
        "Song 6",
        "Song 7",
        "Song 8",
        "Song 9",
        "Song 10",
      ],
      obscurityScore: 72, // example score
    };
  }

  render() {
    const { user, playlist, obscurityScore } = this.state;
    const columns = [];

    for (let i = 0; i < playlist.length; i += 5) {
      const songs = playlist.slice(i, i + 5);
      columns.push(
        <Grid item xs={4} key={i} style={{ padding: "20px" }}>
          <Grid container direction="column" spacing={2}>
            {songs.map((song, index) => (
              <Box
                key={index}
                style={{
                  backgroundColor: "rgba(223,214,239, 0.3)",
                  padding: "40px",
                  marginBottom: "40px",
                  textAlign: "left",
                  fontSize: "8rem",
                  color: "white",
                  fontWeight: "bold",
                  whiteSpace: "nowrap",
                  borderRadius: "20px", // Rounded borders
                  boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)",
                  width: "1300px", // Increased width
                  height: "200px",
                }}
              >
                {song}
              </Box>
            ))}
          </Grid>
        </Grid>
      );
    }

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
            fontSize: "5rem", // Adjust the font size as needed
            padding: "12px 24px", // Adjust the padding for button size
            position: "absolute",
            top: "20px",
            left: "20px",
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
                top: 300,
                left: -1500,
                whiteSpace: "nowrap",
                color: "white",
                fontFamily: "'Roboto', sans-serif",
                fontWeight: "bold",
                borderBottom: "20px solid white",
                paddingBottom: "20px",
                fontSize: "8rem",
              }}
            >
              Your top song playlist
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
                top: 290,
                left: -100,
                color: "white",
                fontFamily: "'Roboto', sans-serif",
                fontWeight: "bold",
                fontSize: "8rem",
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
              top: 200,
              left: -100,
            }}
          >
            {columns}
          </Grid>
        </Grid>
      </div>
    );
  }
}

//   render() {
//     const { user, playlist, obscurityScore } = this.state;

//     return (
//       <div
//         style={{
//           height: "100vh",
//           background: "linear-gradient(to bottom, #3870E5, #5ae67f)",
//           display: "flex",
//           alignItems: "center",
//           justifyContent: "center",
//           position: "relative",
//           fontFamily: "'Roboto', sans-serif",
//         }}
//       >
//         <Typography
//           component="h4"
//           variant="h4"
//           style={{
//             position: "absolute",
//             top: 100,
//             left: -650,
//             color: "white",
//             fontFamily: "'Roboto', sans-serif",
//             fontWeight: "bold",
//             fontSize: "2.5rem",
//             background: "#AD96DC",
//             padding: "10px 20px",
//             borderRadius: "10px",
//             boxShadow: "0 4px 10px rgba(0, 0, 0, 0.2)",
//             whiteSpace: "nowrap",
//           }}
//         >
//           Welcome to your <br /> Niche Song Ranking, {user}!
//         </Typography>
//         <Grid container spacing={1} style={{ height: "100%", width: "auto" }}>
//           <Grid
//             item
//             xs={12}
//             style={{
//               display: "flex",
//               justifyContent: "center",
//               alignItems: "center",
//               position: "relative",
//             }}
//           >
//             <Box
//               style={{
//                 width: "600px", // Adjust the width as needed
//                 background: "#AD96DC",
//                 padding: "20px",
//                 borderRadius: "10px",
//                 boxShadow: "0 4px 50px rgba(0, 0, 0, 0.2)",
//                 marginLeft: "-650px", // Adjust the right margin to position the box
//                 fontSize: "3.5rem",
//               }}
//             >
//               <Typography
//                 component="h4"
//                 variant="h4"
//                 align="center"
//                 style={{
//                   marginBottom: "20px",
//                   color: "white",
//                   fontFamily: "'Roboto', sans-serif",
//                   fontWeight: "bold",
//                   borderBottom: "10px solid white",
//                   paddingBottom: "6px",
//                   fontSize: "2.5rem",
//                 }}
//               >
//                 Your top song playlist
//               </Typography>
//               <ul
//                 style={{
//                   listStyleType: "none",
//                   padding: 0,
//                   textAlign: "left",
//                   color: "white",
//                   fontFamily: "'Roboto', sans-serif",
//                   fontSize: "2rem",
//                 }}
//               >
//                 {playlist.map((song, index) => (
//                   <li
//                     key={index}
//                     style={{
//                       marginBottom: "8px", // Adjust spacing between songs as needed
//                     }}
//                   >
//                     {song}
//                   </li>
//                 ))}
//               </ul>
//             </Box>
//             <Typography
//               component="h4"
//               variant="h4"
//               align="center"
//               style={{
//                 marginLeft: "20px",
//                 whiteSpace: "nowrap",
//                 background: "#AD96DC",
//                 padding: "20px",
//                 borderRadius: "10px",
//                 boxShadow: "10px 10px 10px rgba(0, 0, 0, 0.1)",
//                 position: "absolute",
//                 left: 50,
//                 color: "white",
//                 fontFamily: "'Roboto', sans-serif",
//                 fontWeight: "bold",
//                 fontSize: "2.5rem",
//               }}
//             >
//               Obscurity Score: {obscurityScore}%
//             </Typography>
//           </Grid>
//           <Grid
//             item
//             xs={12}
//             align="center"
//             style={{
//               position: "absolute",
//               bottom: 20,
//               left: "50%",
//               transform: "translateX(-50%)",
//               fontFamily: "'Roboto', sans-serif",
//             }}
//           >
//             <Button
//               color="primary"
//               variant="contained"
//               to="/"
//               component={Link}
//               style={{
//                 fontSize: "1.5rem", // Adjust the font size as needed
//                 padding: "12px 24px", // Adjust the padding for button size
//               }}
//             >
//               Back
//             </Button>
//           </Grid>
//         </Grid>
//       </div>
//     );
//   }
// }
