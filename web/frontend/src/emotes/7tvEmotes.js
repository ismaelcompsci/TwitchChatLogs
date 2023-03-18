import { EmoteSet, Emote } from "./EmoteType";

export default async function get7tvGlobalEmotes() {
  const response = await fetch("https://7tv.io/v3/emote-sets/global");
  const data = await response.json();

  const emotes = EmoteSet(data);
  const GlobalEmotes = [];

  emotes.forEach((emote) => {
    const newEmote = Emote(emote);
    GlobalEmotes.push(newEmote);
  });

  return GlobalEmotes;
}
