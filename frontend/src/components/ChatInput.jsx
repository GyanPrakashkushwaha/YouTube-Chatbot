import { useState, useRef } from "react";

export default function ChatInput({ 
  input, 
  setInput, 
  onSend,
  // youtubeUrl,
  // setYoutubeUrl,
  // isWebSearch,
  // setIsWebSearch,
  // fileInputRef
 }) {
  // States for the new input methods
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [isWebSearch, setIsWebSearch] = useState(false);
  const fileInputRef = useRef(null);

  // Handle file selection
  const handleFileClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      console.log("File uploaded:", file.name);
      // specific file handling logic here
    }
  };

  return (
    <div className="p-5">
      <div className="max-w-4xl mx-auto">
        {/* --- NEW: Input Methods Row --- */}
        <div className="flex flex-wrap items-center gap-2 mb-2 px-1">
          {/* 1. YouTube Input Box */}
          <div className="flex-1 min-w-[200px] relative">
            <input
              type="text"
              placeholder="Paste Youtube url"
              value={youtubeUrl}
              onChange={(e) => setYoutubeUrl(e.target.value)}
              className="w-full px-4 py-2 bg-gray-900 border border-gray-950 rounded-md text-sm text-gray-300 placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-blue-500/50 transition-all shadow-sm"
            />
          </div>

          {/* 2. PDF Uploader (Button/Label style) */}
          <button
            onClick={handleFileClick}
            className="px-4 py-2 bg-gray-900 border border-gray-950 rounded-md text-sm text-gray-400 hover:text-white hover:bg-gray-800 transition-all shadow-sm whitespace-nowrap flex items-center gap-2"
          >
            <span>Upload PDF</span>
            <input
              type="file"
              accept=".pdf"
              ref={fileInputRef}
              onChange={handleFileChange}
              className="hidden"
            />
          </button>

          {/* 3. Web Search Toggler */}
          <button
            onClick={() => setIsWebSearch(!isWebSearch)}
            className={`px-4 py-2 border border-gray-950 rounded-md text-sm transition-all shadow-sm whitespace-nowrap flex items-center gap-2 ${
              isWebSearch
                ? "bg-blue-900/30 text-blue-400 border-blue-500/30"
                : "bg-gray-900 text-gray-400 hover:text-white hover:bg-gray-800"
            }`}
          >
            <span>Web Search</span>
            {/* Optional: Status Indicator Dot */}
            <div
              className={`w-2 h-2 rounded-full ${
                isWebSearch ? "bg-blue-400" : "bg-gray-600"
              }`}
            />
          </button>
        </div>

        {/* --- Existing Chat Input --- */}
        <div className="relative flex items-center gap-3">
          <input
            className="flex-1 px-5 py-3.5 bg-gray-900 text-white placeholder-gray-500 border border-gray-900 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent transition-all shadow-inner"
            placeholder="Ask a question about the video..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && onSend()}
          />
          <button
            className="p-3.5 bg-blue-600 text-white rounded-full hover:bg-blue-500 hover:shadow-lg hover:shadow-blue-500/30 transition-all transform active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
            onClick={onSend}
            disabled={!input.trim()}
            aria-label="Send message"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
              className="w-5 h-5 translate-x-0.5 -translate-y-0.5"
            >
              <path d="M3.105 2.289a.75.75 0 00-.826.95l1.414 4.925A1.5 1.5 0 005.135 9.25h6.115a.75.75 0 010 1.5H5.135a1.5 1.5 0 00-1.442 1.086l-1.414 4.926a.75.75 0 00.826.95 28.896 28.896 0 0015.293-7.154.75.75 0 000-1.115A28.897 28.897 0 003.105 2.289z" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}
