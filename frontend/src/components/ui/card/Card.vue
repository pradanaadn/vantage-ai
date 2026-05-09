<script setup lang="ts">
import { cn } from '@/lib/utils'

const props = defineProps<{
  class?: string
}>()
</script>

<template>
  <div
    :class="
      cn(
        'rounded-xl border border-gray-200 bg-white text-gray-950 shadow-sm',
        props.class,
      )
    "
  >
    <slot />
  </div>
</template>
