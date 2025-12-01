import { useState, useEffect } from "react";
import Sidebar from "./components/Sidebar";
import ChatMessages from "./components/ChatMessages";
import ChatInput from "./components/ChatInput";

import { 
  createIndex, 
  sendChat, 
  extractVideoId,
  loadChatHistory,
  loadVideoHistory
  } from "./services/api";

function App() {
  const [messages, setMessage] = useState([]);
  const [input, setInput] = useState("");
  const [videoId, setVideoId] = useState("f8dhP521DHI");
  const [loadingIndex, setLoadingIndex] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [videoList, setVideoList] = useState([])


  useEffect(() => {
    async function fetchVideos() {
      if (!videoId) return;

      const lsts = await loadVideoHistory(videoId);
      
      if (lsts) {
        setVideoList(lsts);
      }
    }

    fetchVideos();
  }, [videoId]);

  const loadChat = async (vId) => {
    const oldHistory = await loadChatHistory(vId)
    setMessage(oldHistory)
  }

  const handleCreateIndex = async () => {
    const id = extractVideoId(videoId);
    if (!id) return alert("Enter valid video ID");

    setLoadingIndex(true);
    const data = await createIndex(id);
    setLoadingIndex(false);

    if (data.error) alert(data.error);
    else alert("Index created!");

    const oldHistory = await loadChatHistory(id)
    setMessage(oldHistory)
  };

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const id = extractVideoId(videoId);
    
    const userMessage = { sender: "user", text: input }
    setMessage((prev) => [...prev, userMessage]);

    const temp = input;
    setInput("");
    setIsTyping(true);

    const data = await sendChat(id, temp);

    setIsTyping(false);
    const botMessage = { sender: "bot", text: data.error ? data.error : data.reply }
    setMessage((prev) => [...prev, botMessage]);
  };

  return (
    <div className="h-screen w-screen flex bg-black">
      <Sidebar
        videoId={videoId}
        setVideoId={setVideoId}
        loadingIndex={loadingIndex}
        handleCreateIndex={handleCreateIndex}
        videoList={videoList}
        loadChat={loadChat}
      />

      <div className="flex-1 flex flex-col bg-[#1e1e1e]">
        <ChatMessages messages={messages} isTyping={isTyping} />
        <ChatInput input={input} setInput={setInput} onSend={handleSendMessage} />
      </div>
    </div>
  );
}

export default App;
