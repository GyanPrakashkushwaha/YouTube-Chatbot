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


export const loadChatHistory = async (id) => {
    const res = await fetch(`http://127.0.0.1:5000/history/${id}`)
    const data = await res.json()
    
    return data.history || []
}

export const loadVideoHistory = async () => {
    const res = await fetch(`http://127.0.0.1:5000/videos`)
    const data = await res.json()
    
    return data.videos || []
}


// export const loadChatHistory_experiemnt = (id) => {
//     fetch(`http://127.0.0.1:5000/history/${id}`)
//     .then((res) => res.json())
//     .then((data) => data.history || [])
// }
