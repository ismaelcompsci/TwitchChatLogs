const Emote = (emote) => {
  const id = emote.id;
  const name = emote.name;
  const urls = {
    small: emote.urls["1"],
    medium: emote.urls["2"],
    large: emote.urls["4"],
  };
  return { id, name, urls };
};

export default async function getFFzChannelEmotes(id) {
  const response = await fetch(`https://api.frankerfacez.com/v1/room/id/${id}`);
  const data = await response.json();

  const ChannelEmotes = [];

  data.sets["166907"].emoticons.forEach((emote) => {
    const newEmote = Emote(emote);
    ChannelEmotes.push(newEmote);
  });

  return ChannelEmotes;
}
