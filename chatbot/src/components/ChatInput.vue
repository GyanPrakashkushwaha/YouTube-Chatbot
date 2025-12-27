<script setup>
import { computed } from 'vue';

const props = defineProps({
  modelValue: {
    type: String,
    default: ""
  }
})

const emit = defineEmits(["update:modelValue", "send"])

const inputValue = computed({
  get: () => props.modelValue,
  set: (value) => emit("update:modelValue", value)
})

const handleSend = () => {
  // Prevent sending empty messages
  if (!inputValue.value.trim()) return;
  emit('send');
}
</script>

<template>
  <div class="p-4 border-t border-gray-700 bg-[#1e1e1e] flex gap-2">
    <input type="text"
    class="flex-1 px-4 py-2 bg-[#2a2a2a] text-white border border-gray-600 rounded-md focus:outline-none focus:border-blue-500 transition-colors"
    placeholder="Type YOur Message..." v-model="inputValue" @keydown.enter="handleSend"
    />
    <button class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md transition-colors" @click="handleSend">Send</button>
  </div>

</template>