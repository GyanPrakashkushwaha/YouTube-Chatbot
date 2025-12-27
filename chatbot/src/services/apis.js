export const extractVideoId = (input) => {
  try {
    const url = new URL(input);
    return url.searchParams.get("v");
  } catch {
    return input.trim();
  }
};

export const createIndex = async (id) => {
  try {
    const res = await fetch("http://127.0.0.1:5000/index", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ video_id: id }),
    });
    return await res.json();
  } catch (error) {
    console.error("Error creating index:", error);
    return { error: "Failed to connect to backend" };
  }
};

export const sendChat = async (id, message) => {
  try {
    const res = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ video_id: id, message }),
    });
    return await res.json();
  } catch (error) {
    console.error("Error sending chat:", error);
    return { error: "Failed to send message" };
  }
};

export const loadChatHistory = async (id) => {
  try {
    const res = await fetch(`http://127.0.0.1:5000/history/${id}`);
    const data = await res.json();
    return data.history || [];
  } catch (error) {
    console.error("Error loading history:", error);
    return [];
  }
};

export const loadVideoHistory = async () => {
  try {
    const res = await fetch(`http://127.0.0.1:5000/videos`);
    const data = await res.json();
    return data.videos || [];
  } catch (error) {
    console.error("Error loading video list:", error);
    return [];
  }
};