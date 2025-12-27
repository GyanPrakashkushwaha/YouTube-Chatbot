<script setup>
import { ref, watch, nextTick } from 'vue';

const props = defineProps({
  messages: {
    type: Array,
    default: () => []
  },
  isTyping: {
    type: Boolean,
    default: false
  }
});

// Reference to the scrollable container
const containerRef = ref(null);

// Auto-scroll to bottom when messages change
watch(
  () => props.messages.length, 
  async () => {
    await nextTick(); // Wait for DOM update
    if (containerRef.value) {
      containerRef.value.scrollTo({
        top: containerRef.value.scrollHeight,
        behavior: 'smooth'
      });
    }
  }
);
</script>

<template>
  <div ref="containerRef" class="flex-1 p-6 overflow-y-auto space-y-4">
    <div 
      v-for="(m, i) in messages" 
      :key="i" 
      class="flex"
      :class="m.sender === 'user' ? 'justify-end' : 'justify-start'"
    >
      <div
        class="w-[85%] p-4 rounded-lg text-white transition-colors"
        :class="m.sender === 'user' ? 'bg-[#2a2a2a]' : 'bg-[#3a3a3a]'"
      >
        {{ m.text }}
      </div>
    </div>

    <div v-if="isTyping" class="flex justify-start">
      <div class="w-[85%] bg-[#3a3a3a] p-4 rounded-lg text-gray-400 animate-pulse">
        typing...
      </div>
    </div>
  </div>
</template>