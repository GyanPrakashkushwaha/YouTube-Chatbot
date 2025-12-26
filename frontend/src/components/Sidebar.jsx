export default function Sidebar({
  videoId,
  setVideoId,
  loadingIndex,
  handleCreateIndex,
  videoList,
  loadChat,
  resetChat
}) {
  return (
    <div className="flex flex-col w-72 bg-gray-900 text-gray-100 p-5 border-r border-gray-800 shadow-lg z-20">
      <div className="mb-6">
        <h2 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
          YT ChatBot
        </h2>
        <p className="text-xs text-gray-500 mt-1">Talk to your videos</p>

        <button className="pl-18 pr-18 pt-2 pb-2 m-2 rounded-xl bg-gray-800 hover:bg-gray-750 border border-gray-700 hover:border-blue-500/50 transition-all duration-200 cursor-pointer shadow-sm hover:shadow-md group"
        onClick={() => resetChat()}
        >
          New Chat
        </button>
      </div>

      <div className="flex-1 overflow-y-auto space-y-3 pr-2 scrollbar-thin">
        <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
          History
        </h3>
        {videoList.length === 0 && (
          <div className="text-sm text-gray-600 italic">No history yet.</div>
        )}
        {videoList.map((v, i) => (
          <div
            key={i}
            className="p-3 rounded-xl bg-gray-800 hover:bg-gray-750 border border-gray-700 hover:border-blue-500/50 transition-all duration-200 cursor-pointer shadow-sm hover:shadow-md group"
            onClick={() => loadChat(v.id)}
          >
            <div className="text-sm text-gray-300 font-medium group-hover:text-white line-clamp-2">
              {v.title || v.id}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 pt-4 border-t border-gray-800">
        <label className="text-xs font-medium text-gray-400 mb-2 block">
          Add New Video
        </label>
        <input
          type="text"
          placeholder="Video ID or URL"
          className="w-full px-4 py-2.5 rounded-lg bg-gray-800 border border-gray-700 text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent transition-all placeholder-gray-600"
          value={videoId}
          onChange={(e) => setVideoId(e.target.value)}
        />

        <button
          className={`w-full mt-3 py-2.5 rounded-lg text-sm font-semibold text-white shadow-lg transition-all transform active:scale-95 ${
            loadingIndex
              ? "bg-gray-700 opacity-60 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-500 hover:shadow-blue-500/20"
          }`}
          onClick={handleCreateIndex}
          disabled={loadingIndex}
        >
          {loadingIndex ? (
            <span className="flex items-center justify-center gap-2">
              <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
              Indexing...
            </span>
          ) : (
            "Create Index"
          )}
        </button>
      </div>
    </div>
  );
}
