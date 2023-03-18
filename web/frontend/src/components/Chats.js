import { Grid, Button } from "@mui/material";
import React, { useEffect, useState } from "react";
import APIService from "./APIService";
import LogContainer from "./LogContainer";
import { useNavigate } from "react-router-dom";
import getEmotes from "../emotes/getEmotes";

export default function Chats(props) {
  const [messages, setMessages] = useState([]);
  const [clickedButtons, setClickedButtons] = useState([]);
  const navigate = useNavigate();
  const [emotes, setEmotes] = useState([]);

  useEffect(() => {
    const button = document.getElementById("chat-button-0");
    if (button) {
      button.click();
    }
  }, []);

  const emotePasser = async (id) => {
    const emotes = await getEmotes(id);

    return emotes;
  };

  const handleChatButtonClick = async (e, date, index) => {
    const data = await APIService.ChannelUserDateLogs(
      props.channel,
      props.username,
      date.year,
      date.month
    );

    if (data.code === 204) {
      alert("No Logs Found");
      navigate("/");
      return;
    }

    setMessages((prevMessages) => [...prevMessages, { index, data }]);
    setClickedButtons((prevClickedButtons) => [...prevClickedButtons, index]);
    const emotes_ = await emotePasser(data.messages[0].tags.room_id);
    setEmotes(emotes_);
  };

  return (
    <Grid container spacing={3} padding="2rem" paddingTop="0" width="100%">
      <Grid item xs={12}>
        {props.chats.logs.map((chat, index) => (
          <Grid
            container
            item
            xs={12}
            align="left"
            borderRadius="3px"
            padding="0.5rem"
            marginTop="3rem"
            key={`${chat.year}-${chat.month}`}
          >
            {clickedButtons.includes(index) ? (
              <Grid item xs={12}>
                <LogContainer
                  messages={messages.find((m) => m.index === index)?.data}
                  emotes={emotes}
                />
              </Grid>
            ) : (
              <Grid item xs={12}>
                <Grid sx={{ display: "flex", alignItems: "center", p: 2 }}>
                  <Button
                    id={`chat-button-${index}`}
                    onClick={(e) => handleChatButtonClick(e, chat, index)}
                    color="primary"
                    size="large"
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
                  >
                    {`SEARCH ${chat.year}/${chat.month}`}
                  </Button>
                </Grid>
              </Grid>
            )}
          </Grid>
        ))}
      </Grid>
    </Grid>
  );
}
