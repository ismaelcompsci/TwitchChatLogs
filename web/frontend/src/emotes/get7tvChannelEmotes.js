import { EmoteSet, Emote } from "./EmoteType";

export default async function get7tChannelEmotes(id) {
  const response = await fetch(`https://7tv.io/v3/users/twitch/${id}`);
  const data = await response.json();

  const emotes = EmoteSet(data.emote_set);

  const ChannelEmotes = [];

  emotes.forEach((emote) => {
    const newEmote = Emote(emote);
    ChannelEmotes.push(newEmote);
  });

  return ChannelEmotes;
}
