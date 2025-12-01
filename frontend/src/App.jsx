import { useState } from "react";
import "./App.css";
import axios from "axios";

function App() {
  const [messages, setMessage] = useState([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [videoId, setVideoId] = useState("");
  const [loadingIndex, setLoadingIndex] = useState(false)


  const handleCreateIndex = async () => {
    const id = extractVideoId(videoId)
    if (!id){
      alert("Please enter a valid youtube Video ID or URL");
      return;
    }
    setLoadingIndex(true)
    const res = await fetch("http://127.0.0.1:5000/index", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({video_id: id})
    })
    .then((res) => res.json())  // <-- WAIT FOR JSON HERE
    .then((data) => { // <-- NOW 'data' is the JSON
      console.log("index response:", data)
      setLoadingIndex(false)
      if (data.error) {
        alert("Error: " + data.error);
      } else {
        alert("Index created successfully!");
      }
    })
    .catch((err) => {
      setLoadingIndex(false)
      console.error(err)
      alert('backend not responding...')
    })
    
  };

  const extractVideoId = (input) => {
    try {
      // If user pastes full YouTube URL
      const url = new URL(input);
      return url.searchParams.get("v");
    } catch {
      // If it's already a pure video ID
      return input.trim();
    }
  };




  const inputFunc = async () => {
    if (input.trim() === "") return;

    setMessage((prev) => [...prev, { sender: "user", text: input }]);

    const tempInput = input

    setInput("");
    setIsTyping(true);

    const id = extractVideoId(videoId);

    if (!id){
      setIsTyping(false)
      setMessage((prev) => [
        ...prev,
        {sender: "bot", "text": "please enter a video ID first"}
      ])
      return
    }

    fetch("http://127.0.0.1:5000/chat", {
      method : "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        video_id: id,
        message: tempInput
      })
    })
    .then((res) => res.json())
    .then((data) => {
      setIsTyping(false)

      if (data.error){
        setMessage((prev) => [
          ...prev,
          {sender: "bot", text: "Error: " + data.error}
        ]);
      } else{
        setMessage((prev) => [
          ...prev,
          {sender: "bot", text: data.reply}
        ])
      }
    })
    .catch((err) => {
      console.error(err)
      setIsTyping(false)
      setMessage((prev) => [
        ...prev,
        {sender: "bot", text: "Backend not responding 😭"}
      ])
    })

  };

  return (
    <div className="h-screen w-screen flex bg-black">
      {/* LEFT SIDEBAR */}
      <div className="w-64 bg-[#111111] text-white p-4 border-r border-gray-700">
        <h2 className="text-xl font-bold mb-6">My Chatbot</h2>
        <div className="space-y-4">
          {/* Video ID input */}
          <input
            type="text"
            placeholder="Enter video ID or URL"
            className={`w-full px-3 py-2 rounded bg-[#2a2a2a] text-white border border-gray-700 focus:outline-none`}
            value={videoId}
            onChange={(e) => setVideoId(e.target.value)}
            />

          {/* Create Index button */}
          <button
            className={`w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded ${loadingIndex? "opacity-60 cursor-not-allowed": ""}`}
            onClick={handleCreateIndex}
            disabled = {loadingIndex}
          >
            {loadingIndex ? "Indexing..." : "Create Index"}
          </button>
        </div>
      </div>

      {/* RIGHT CHAT AREA */}
      <div className="flex-1 flex flex-col bg-[#1e1e1e]">
        {/* Chat messages */}
        <div className="flex-1 p-6 overflow-y-auto space-y-4">
          {/* User Message */}

          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${
                message.sender === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`w-[85%] p-4 rounded-lg  text-white ${
                  message.sender === "user" ? "bg-[#2a2a2a]" : "bg-[#3a3a3a]"
                }`}
              >
                <p>{message.text}</p>
              </div>
            </div>
          ))}

          {isTyping && (
            <div className="flex justify-start">
              <div className="w-[85%] bg-[#3a3a3a] text-gray-200 p-4 rounded-lg">
                <div className="flex space-x-1">
                  <span className="dot h-2 w-2 bg-gray-400 rounded-full inline-block"></span>
                  <span className="dot h-2 w-2 bg-gray-400 rounded-full inline-block"></span>
                  <span className="dot h-2 w-2 bg-gray-400 rounded-full inline-block"></span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input area */}
        <div className="p-4 border-t border-gray-700 bg-[#1e1e1e] flex gap-2">
          <input
            className="flex-1 px-4 py-2 bg-[#2a2a2a] text-white border border-gray-600 rounded-md focus:outline-none"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") inputFunc();
            }}
          />
          <button
            className="px-4 py-2 bg-blue-600 text-white rounded-md"
            onClick={inputFunc}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
