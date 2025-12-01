export default function Sidebar({
  videoId,
  setVideoId,
  loadingIndex,
  handleCreateIndex,
  videoList,
  loadChat
}) {
  return (
    <div className="flex flex-col w-64 bg-[#111111] text-white p-4 border-r border-gray-700">
      <h2 className="text-xl font-bold mb-6">My Chatbot</h2>

      <div className="mt-6 space-y-2">
        {videoList.map((v, i) => (
          <div
            key={i}
            className="p-3 rounded-lg bg-[#1a1a1a] border border-[#333] hover:border-blue-500 hover:bg-[#222] transition-all cursor-pointer"
            onClick={() => (loadChat(v.id))}
          >
            <div className="text-sm text-gray-300">{v.id}</div>
          </div>
        ))}
      </div>

    
      <div className="mt-auto p-4">
        <input
          type="text"
          placeholder="Enter video ID or URL"
          className="w-full px-3 py-2 rounded bg-[#2a2a2a]"
          value={videoId}
          onChange={(e) => setVideoId(e.target.value)}
        />

        <button
          className={`w-full bg-blue-600 mt-4 text-white py-2 rounded ${
            loadingIndex ? "opacity-60 cursor-not-allowed" : ""
          }`}
          onClick={handleCreateIndex}
          disabled={loadingIndex}
        >
          {loadingIndex ? "Indexing..." : "Create Index"}
        </button>
      </div>
      
    </div>
  );
}
