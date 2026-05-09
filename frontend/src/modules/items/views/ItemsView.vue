<template>
  <div class="items-view">
    <h1>Items from API</h1>
    <div v-if="itemsStore.loading">Loading...</div>
    <ul v-else>
      <li v-for="item in itemsStore.items" :key="item.id">
        {{ item.name }}
      </li>
    </ul>
    <button @click="itemsStore.fetchItems()">Refresh</button>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useItemsStore } from '../store/itemsStore';

const itemsStore = useItemsStore();

onMounted(() => {
  itemsStore.fetchItems();
});
</script>

<style scoped>
.items-view {
  padding: 20px;
}
</style>
