export default function ChatMessages({ messages, isTyping }) {
  return (
    <div className="flex-1 p-6 overflow-y-auto space-y-4">
      {messages.map((m, i) => (
        <div key={i} className={`flex ${m.sender === "user" ? "justify-end" : "justify-start"}`}>
          <div
            className={`w-[85%] p-4 rounded-lg text-white ${
              m.sender === "user" ? "bg-[#2a2a2a]" : "bg-[#3a3a3a]"
            }`}
          >
            {m.text}
          </div>
        </div>
      ))}

      {isTyping && (
        <div className="flex justify-start">
          <div className="w-[85%] bg-[#3a3a3a] p-4 rounded-lg">
            typing...
          </div>
        </div>
      )}
    </div>
  );
}
