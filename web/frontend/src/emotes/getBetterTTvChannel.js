const Emote = (emote) => {
  const id = emote.id;
  const name = emote.code;
  const urls = {
    small: `https://cdn.betterttv.net/emote/${emote.id}/1x`,
    medium: `https://cdn.betterttv.net/emote/${emote.id}/2x`,
    large: `https://cdn.betterttv.net/emote/${emote.id}/3x`,
  };
  return { id, name, urls };
};

export default async function getBetterTTvChannelEmotes(room_id) {
  const response = await fetch(
    `https://api.betterttv.net/3/cached/users/twitch/${room_id}`
  );
  const data = await response.json();

  const ChannelEmotes = [];

  [...data.channelEmotes, ...data.sharedEmotes].forEach((emote) => {
    const newEmote = Emote(emote);
    ChannelEmotes.push(newEmote);
  });

  return ChannelEmotes;
}
