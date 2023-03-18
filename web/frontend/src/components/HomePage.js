import React from "react";
import { Grid, Button, TextField, Box } from "@mui/material";

import { useState } from "react";
import Chats from "./Chats";
import APIService from "./APIService";

export default function HomePage() {
  const [inputChannel, setInputChannel] = useState("");
  const [inputUsername, setInputUsername] = useState("");

  const [channelLogs, setChannelLogs] = useState([]);

  const [visible, setVisible] = useState(false);

  const [errorChannelText, setErrorChannelText] = useState("");
  const [errorUsernameText, setErrorUsernameText] = useState("");

  const [hideSearchButton, setHideSearchButton] = useState(true);

  const handleSearchButtonClicked = async (e) => {
    if (inputChannel.length === 0 || inputUsername.length === 0) {
      hideSearchButton(true);
    }
    e.preventDefault();
    setChannelLogs([]);
    setVisible(false);

    const data = await APIService.AvailableLogs(inputChannel);

    setChannelLogs(data);
    setVisible(true);
  };

  const handleChannelChange = (e) => {
    if (e.target.value.length > 0) {
      setErrorChannelText("");
      setHideSearchButton(false);
    } else {
      setErrorChannelText("Please Input a Channel");
      setHideSearchButton(true);
    }

    setInputChannel(e.target.value);
  };
  const handleUsernameChange = (e) => {
    if (e.target.value.length > 0) {
      setErrorUsernameText("");
      setHideSearchButton(false);
    } else {
      setErrorUsernameText("Please Input a Username");
      setHideSearchButton(true);
    }

    setInputUsername(e.target.value);
  };

  return (
    <Grid container spacing={3}>
      <Box
        bgcolor={"#0a0b0c"}
        width="100%"
        align="center"
        paddingBottom={4}
        paddingTop={3}
      >
        <Grid
          item
          xs={12}
          align="center"
          justifyContent="center"
          display="inline-block"
        >
          <Box bgcolor="#1F1B24" padding={3} borderRadius={5}>
            <TextField
              helperText={errorChannelText}
              label="Channel"
              placeholder="Enter Channel Name"
              variant="filled"
              // style={{ padding: "0px 10px" }}
              sx={{
                background: "#332940",
                input: { color: "#F0F0ff" },
                "& label": {
                  color: "#772CE8 ",
                },
              }}
              onChange={handleChannelChange}
            />
            <TextField
              helperText={errorUsernameText}
              label="Username"
              placeholder="Enter Username Name"
              sx={{
                background: "#332940",
                input: {
                  color: "#F0F0ff",
                },
                "& label": {
                  color: "#772CE8",
                },
              }}
              variant="filled"
              onChange={handleUsernameChange}
            />
            <Button
              disabled={hideSearchButton}
              variant="contained"
              style={{ minHeight: "55px" }}
              sx={{
                marginLeft: "10px",
                background: "#772CE8",
                "&:hover": {
                  bgcolor: "#9146FF",
                  color: "white",
                },
              }}
              onClick={handleSearchButtonClicked}
            >
              Search
            </Button>
          </Box>
        </Grid>
      </Box>
      {visible && (
        <Chats
          channel={inputChannel}
          username={inputUsername}
          chats={channelLogs}
        />
      )}
    </Grid>
  );
}
