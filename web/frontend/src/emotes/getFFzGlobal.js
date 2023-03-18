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

export default async function getFFzGlobalEmotes() {
  const response = await fetch(`https://api.frankerfacez.com/v1/set/global`);
  const data = await response.json();

  const GlobalEmotes = [];

  data.sets["3"].emoticons.forEach((emote) => {
    const newEmote = Emote(emote);
    GlobalEmotes.push(newEmote);
  });

  return GlobalEmotes;
}
