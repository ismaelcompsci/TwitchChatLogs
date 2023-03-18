export default class APIService {
  static async AvailableLogs(channel) {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/list/all/channel/${channel}/users?${new URLSearchParams(
          { reverse: true }
        )}`,
        {
          headers: { "Content-Type": "application/json" },
        }
      );

      const data = await response.json();

      return data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  static async ChannelUserDateLogs(channel, username, year, month) {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/channel/${channel}/username/${username}/${year}/${month}?${new URLSearchParams(
          { reverse: true }
        )}`,
        {
          headers: { "Content-Type": "application/json" },
        }
      );
      if (response.status === 204) {
        return { detail: "No Logs Found", code: 204 };
      }

      const data = await response.json();

      return data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }
}
