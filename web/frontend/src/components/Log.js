import { Box, Typography } from "@mui/material";

import React from "react";
import renderTextWithEmotes from "../emotes/renderTextWithEmotes";

const DATEOPTIONS = {
  // you can use undefined as first argument
  year: "numeric",
  month: "2-digit",
  day: "2-digit",
  hour: "2-digit",
  minute: "2-digit",
  hourCycle: "h12",
};

const MessageText = ({ text, emotes }) => {
  return (
    <Typography marginLeft="5px" color="rgb(220, 219, 216);">
      {renderTextWithEmotes(text, emotes)}
    </Typography>
  );
};

const MessageDisplayName = ({ display_name, color }) => {
  return (
    <Typography marginLeft="5px" color={color} fontWeight="bold">
      {display_name}:
    </Typography>
  );
};

const MessageDateTime = ({ time }) => {
  return (
    <Typography
      fontSize={"small"}
      color="#F0F0ff"
      fontWeight={100}
      fontFamily="monospace"
    >
      {new Date(Number(time))
        .toLocaleString("en-GB", DATEOPTIONS)
        .replace(",", " - ")}
    </Typography>
  );
};

export default function LogMessage(props) {
  const { log: Line, emotes: Emotes } = props;

  return (
    <Box
      whiteSpace="nowrap"
      display="flex"
      alignItems="center"
      flexDirection="row"
      justifyContent="center"
    >
      <span style={{ color: "#9146FF", display: "block" }}>[</span>
      <MessageDateTime time={Line.tags.tmi_sent_ts} />
      <span style={{ color: "#9146FF", display: "block" }}>]</span>
      <MessageDisplayName
        display_name={Line.display_name}
        color={Line.tags.color}
      />
      <MessageText text={Line.text} emotes={Emotes} />
    </Box>
  );
}
