export default function ChatInput({ input, setInput, onSend }) {
  return (
    <div className="p-4 border-t border-gray-700 bg-[#1e1e1e] flex gap-2">
      <input
        className="flex-1 px-4 py-2 bg-[#2a2a2a] text-white border border-gray-600 rounded-md"
        placeholder="Type your message..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && onSend()}
      />
      <button
        className="px-4 py-2 bg-blue-600 text-white rounded-md"
        onClick={onSend}
      >
        Send
      </button>
    </div>
  );
}
