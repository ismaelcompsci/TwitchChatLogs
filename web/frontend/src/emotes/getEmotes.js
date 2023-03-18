import get7tvGlobalEmotes from "./7tvEmotes";
import get7tvChannelEmotes from "./get7tvChannelEmotes";
import getBetterTTvChannelEmotes from "./getBetterTTvChannel";
import getBetterTTvGlobalEmotes from "./getBetterTTvGlobal";
import getFFzChannelEmotes from "./getFFzChannel";
import getFFzGlobalEmotes from "./getFFzGlobal";

export default async function getEmotes(room_id) {
  console.log("EMOTE API CALLEDD");
  const emotes = await get7tvGlobalEmotes();
  const emotes_ = await get7tvChannelEmotes(room_id);
  const bttvg = await getBetterTTvGlobalEmotes();
  const bttvc = await getBetterTTvChannelEmotes(room_id);
  const ffzg = await getFFzGlobalEmotes();
  const ffzh = await getFFzChannelEmotes(room_id);

  return [...emotes, ...emotes_, ...bttvg, ...bttvc, ...ffzg, ...ffzh];
}
