export const EmoteSet = (data) => {
  const emotes = data.emotes;
  return emotes;
};

export const Emote = (emote) => {
  const id = emote.id;
  const name = emote.name;

  const urls = {
    small: `https://cdn.7tv.app/emote/${emote.id}/${emote.data.host.files[1].name}`,
    medium: `https://cdn.7tv.app/emote/${emote.id}/${emote.data.host.files[3].name}`,
    large: `https://cdn.7tv.app/emote/${emote.id}/${emote.data.host.files[5].name}`,
    xlarge: `https://cdn.7tv.app/emote/${emote.id}/${emote.data.host.files[7].name}`,
  };

  return { id, name, urls };
};
