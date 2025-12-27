<script setup>
import { computed } from 'vue';

const props = defineProps({
  videoId: {
    type: String,
    default: ""
  },
  loadingIndex: {
    type: Boolean,
    default: false
  },
  videoList: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['update:videoId', 'createIndex', 'loadChat']);

// Computed property for v-model binding
const localVideoId = computed({
  get: () => props.videoId,
  set: (val) => emit('update:videoId', val)
});
</script>

<template>
  <div class="flex flex-col w-64 bg-[#111111] text-white p-4 border-r border-gray-700 h-full">
    <h2 class="text-xl font-bold mb-6">My Chatbot</h2>

    <div class="mt-6 space-y-2 overflow-y-auto flex-1">
      <div
        v-for="(v, i) in videoList"
        :key="i"
        class="p-3 rounded-lg bg-[#1a1a1a] border border-[#333] hover:border-blue-500 hover:bg-[#222] transition-all cursor-pointer"
        @click="$emit('loadChat', v.id)"
      >
        <div class="text-sm text-gray-300 truncate" :title="v.title">
          {{ v.title }}
        </div>
      </div>
    </div>

    <div class="mt-auto p-4 border-t border-gray-800">
      <input
        type="text"
        placeholder="Enter video ID or URL"
        class="w-full px-3 py-2 rounded bg-[#2a2a2a] text-white border border-transparent focus:border-blue-500 focus:outline-none transition-colors"
        v-model="localVideoId"
      />

      <button
        class="w-full bg-blue-600 mt-4 text-white py-2 rounded font-medium hover:bg-blue-700 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
        :disabled="loadingIndex"
        @click="$emit('createIndex')"
      >
        {{ loadingIndex ? "Indexing..." : "Create Index" }}
      </button>
    </div>
  </div>
</template>