import { Grid, ListItem } from "@mui/material";
import React from "react";
import { FixedSizeList as List } from "react-window";
import LogMessage from "./Log";

export default function LogContainer(props) {
  const logs = props.messages.messages;

  const Row = ({ index, style }) => (
    <ListItem style={{ ...style, whiteSpace: "nowrap" }}>
      <LogMessage log={logs[index]} emotes={props.emotes}></LogMessage>
    </ListItem>
  );

  return (
    <Grid container spacing={1} backgroundColor="#332940" marginLeft="20px">
      <Grid item xs={12} align="center">
        <List
          className="List"
          height={600}
          itemCount={logs.length}
          itemSize={20}
          width={"100%"}
        >
          {Row}
        </List>
      </Grid>
    </Grid>
  );
}
