<script setup>
import { ref, watch, onMounted } from 'vue';
import Sidebar from './components/Sidebar.vue';
import ChatMessages from './components/ChatMessages.vue';
import ChatInput from './components/ChatInput.vue';

import { 
  createIndex, 
  sendChat, 
  extractVideoId, 
  loadChatHistory, 
  loadVideoHistory 
} from './services/apis';

// --- State ---
const messages = ref([]);
const input = ref("");
const videoId = ref("f8dhP521DHI");
const loadingIndex = ref(false);
const isTyping = ref(false);
const videoList = ref([]);

// --- API Interactions ---

// Fetch available videos
const fetchVideos = async () => {
  const lsts = await loadVideoHistory();
  if (lsts) {
    videoList.value = lsts;
  }
};

// Load chat history for a specific video
const loadChat = async (vId) => {
  const oldHistory = await loadChatHistory(vId);
  videoId.value = vId;
  messages.value = oldHistory;
};

// Create a new index (Vector Store)
const handleCreateIndex = async () => {
  const id = extractVideoId(videoId.value);
  if (!id) return alert("Enter valid video ID");

  loadingIndex.value = true;
  const data = await createIndex(id);
  loadingIndex.value = false;

  if (data.error) {
    alert(data.error);
  } else {
    alert("Index created!");
    // Refresh the video list after creating a new index
    await fetchVideos();
    // Load the history for this new video
    const oldHistory = await loadChatHistory(id);
    messages.value = oldHistory;
  }
};

// Send a message to the bot
const handleSendMessage = async () => {
  if (!input.value.trim()) return;

  const id = extractVideoId(videoId.value);
  
  // Optimistic UI update
  const userMessage = { sender: "user", text: input.value };
  messages.value.push(userMessage);

  const tempInput = input.value;
  input.value = ""; // Clear input immediately
  isTyping.value = true;

  // Send to backend
  const data = await sendChat(id, tempInput);

  isTyping.value = false;
  const botMessage = { 
    sender: "bot", 
    text: data.error ? data.error : data.reply 
  };
  messages.value.push(botMessage);
};

// --- Lifecycle & Watchers ---

// Initial load
onMounted(() => {
  fetchVideos();
  // Load default video history if exists
  if (videoId.value) {
    loadChat(videoId.value);
  }
});

// Re-fetch video list if videoId changes (mimicking original React behavior)
watch(videoId, () => {
  fetchVideos();
});
</script>

<template>
  <div class="h-screen w-screen flex bg-black">
    <Sidebar
      v-model:videoId="videoId"
      :loadingIndex="loadingIndex"
      :videoList="videoList"
      @createIndex="handleCreateIndex"
      @loadChat="loadChat"
    />

    <div class="flex-1 flex flex-col bg-[#1e1e1e]">
      <ChatMessages 
        :messages="messages" 
        :isTyping="isTyping" 
      />
      
      <ChatInput 
        v-model="input" 
        @send="handleSendMessage" 
      />
    </div>
  </div>
</template>