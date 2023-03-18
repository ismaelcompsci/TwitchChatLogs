export default function renderTextWithEmotes(text, emotes) {
  const words = text.split(" ");

  const wordsWithEmotes = [];

  for (let i = 0; i < words.length; i++) {
    const word = words[i];
    const emote = emotes.find((e) => e.name === word);

    if (emote) {
      wordsWithEmotes.push(
        <img
          key={i}
          src={emote.urls.medium}
          alt={emote.name}
          style={{
            maxHeight: "18px",
            margin: "0 2px",
            marginBottom: "-2px",
            width: "auto",
          }}
        />
      );
    } else {
      wordsWithEmotes.push(word + " ");
    }
  }
  return wordsWithEmotes;
}
