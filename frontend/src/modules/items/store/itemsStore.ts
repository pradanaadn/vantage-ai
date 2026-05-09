import { defineStore } from 'pinia';
import { itemsService } from '../services/itemsService';

export const useItemsStore = defineStore('items', {
  state: () => ({
    items: [] as any[],
    loading: false,
  }),
  actions: {
    async fetchItems() {
      this.loading = true;
      try {
        this.items = await itemsService.getItems();
      } finally {
        this.loading = false;
      }
    },
  },
});
