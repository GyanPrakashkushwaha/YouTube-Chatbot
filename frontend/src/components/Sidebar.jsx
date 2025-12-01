export default function Sidebar({
  videoId,
  setVideoId,
  loadingIndex,
  handleCreateIndex
}) {
  return (
    <div className="w-64 bg-[#111111] text-white p-4 border-r border-gray-700">
      <h2 className="text-xl font-bold mb-6">My Chatbot</h2>

      <input
        type="text"
        placeholder="Enter video ID or URL"
        className="w-full px-3 py-2 rounded bg-[#2a2a2a]"
        value={videoId ? videoId : setVideoId("f8dhP521DHI")}
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
  );
}
