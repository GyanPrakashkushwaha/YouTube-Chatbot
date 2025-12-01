export const extractVideoId = (input) => {
  try {
    const url = new URL(input);
    return url.searchParams.get("v");
  } catch {
    return input.trim();
  }
};

export const createIndex = async (id) => {
  const res = await fetch("http://127.0.0.1:5000/index", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ video_id: id })
  });
  return res.json();
};

export const sendChat = async (id, message) => {
  const res = await fetch("http://127.0.0.1:5000/chat", {
    method : "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ video_id: id, message })
  });
  return res.json();
};
