import { useEffect, useRef } from "react";

export default function ChatMessages({ messages, isTyping }) {
  const bottomRef = useRef(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  return (
    <div className="flex-1 p-6 overflow-y-auto space-y-6">
      {messages.length === 0 && (
        <div className="h-full flex flex-col items-center justify-center text-gray-500 opacity-50 select-none">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
          <p>Start the conversation</p>
        </div>
      )}

      {messages.map((m, i) => (
        <div 
          key={i} 
          className={`flex w-full ${m.sender === "user" ? "justify-end" : "justify-start"}`}
        >
          <div
            className={`max-w-[80%] px-5 py-3.5 shadow-md leading-relaxed ${
              m.sender === "user" 
                ? "bg-blue-600 text-white rounded-2xl rounded-tr-sm" 
                : "bg-gray-700 text-gray-100 rounded-2xl rounded-tl-sm"
            }`}
          >
            {m.text}
          </div>
        </div>
      ))}

      {isTyping && (
        <div className="flex justify-start">
          <div className="bg-gray-700 px-4 py-3 rounded-2xl rounded-tl-sm shadow-md flex items-center space-x-1">
            <div className="w-2 h-2 bg-gray-400 rounded-full dot"></div>
            <div className="w-2 h-2 bg-gray-400 rounded-full dot"></div>
            <div className="w-2 h-2 bg-gray-400 rounded-full dot"></div>
          </div>
        </div>
      )}
      <div ref={bottomRef} />
    </div>
  );
}