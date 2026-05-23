<script setup lang="ts">
interface Props {
  color?: string;
  intensity?: 'low' | 'medium' | 'high';
}

withDefaults(defineProps<Props>(), {
  color: 'emerald-100',
  intensity: 'medium'
});
</script>

<template>
  <div 
    class="absolute pointer-events-none blur-[140px] animate-glow-pulse"
    :class="[
      color.startsWith('bg-') ? color : `bg-${color}`,
      {
        'opacity-20': intensity === 'low',
        'opacity-40': intensity === 'medium',
        'opacity-60': intensity === 'high'
      }
    ]"
  ></div>
</template>

