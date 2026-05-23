<script setup lang="ts">
defineProps<{
  hover?: boolean;
}>();
</script>

<template>
  <div 
    class="bg-vantage-dark border border-slate-200/60 rounded-3xl p-8 relative overflow-hidden transition-all duration-500 shadow-sm"
    :class="{ 'hover:border-emerald-200 hover:shadow-xl hover:shadow-emerald-500/5 hover:-translate-y-0.5': hover }"
  >
    <div class="relative z-10">
      <slot />
    </div>
    <!-- Subtle Gradient Background -->
    <div class="absolute inset-0 bg-gradient-to-br from-emerald-50/[0.03] to-transparent pointer-events-none"></div>
  </div>
</template>


