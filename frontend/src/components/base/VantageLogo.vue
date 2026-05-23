<template>
  <svg :class="className" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <!-- Base gradient for V structure -->
      <linearGradient id="vantage-logo-grad-1" x1="0%" y1="100%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#059669" /> <!-- Vantage Emerald Accent -->
        <stop offset="100%" stop-color="#10b981" /> <!-- Vantage Emerald Glow -->
      </linearGradient>
      
      <!-- Modern overlay cyan-teal gradient -->
      <linearGradient id="vantage-logo-grad-2" x1="100%" y1="100%" x2="0%" y2="0%">
        <stop offset="0%" stop-color="#34d399" />
        <stop offset="100%" stop-color="#06b6d4" />
      </linearGradient>

      <!-- Soft ambient glow -->
      <filter id="vantage-logo-glow" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="5" result="blur" />
        <feComposite in="SourceGraphic" in2="blur" operator="over" />
      </filter>
    </defs>

    <!-- Isometric Left Arm representing high starting vantage point -->
    <path d="M22 20 L44 76 L54 76 L32 20 Z" fill="url(#vantage-logo-grad-1)" />

    <!-- Isometric Right Arm representing smart growth trajectory -->
    <path d="M78 20 L46 76 L56 76 L88 20 Z" fill="url(#vantage-logo-grad-2)" opacity="0.95" />

    <!-- Central Glowing Diamond Core representing intelligent insights (AI) -->
    <path d="M50 32 L62 54 L50 64 L38 54 Z" fill="#ffffff" opacity="0.9" filter="url(#vantage-logo-glow)" />

    <!-- Golden Sparkle representing foresight and elite capability -->
    <path d="M78 12 L80.5 17.5 L86 20 L80.5 22.5 L78 28 L75.5 22.5 L70 20 L75.5 17.5 Z" fill="#f59e0b" />
  </svg>
</template>

<script setup lang="ts">
defineProps({
  className: {
    type: String,
    default: 'w-6 h-6'
  }
});
</script>
