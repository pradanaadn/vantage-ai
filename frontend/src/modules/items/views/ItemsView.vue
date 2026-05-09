<template>
  <div class="min-h-screen bg-gray-50/50 p-8">
    <div class="max-w-5xl mx-auto">
      <header class="mb-10 flex justify-between items-end">
        <div>
          <div class="flex items-center gap-2 mb-2">
            <div class="p-2 bg-indigo-600 rounded-lg shadow-indigo-200 shadow-lg">
              <Package class="w-5 h-5 text-white" />
            </div>
            <span class="text-sm font-semibold text-indigo-600 uppercase tracking-wider">Inventory System</span>
          </div>
          <h1 class="text-4xl font-bold text-gray-900 tracking-tight">Resource Catalog</h1>
          <p class="text-gray-500 mt-2 text-lg">Manage and monitor your digital assets in real-time.</p>
        </div>
        
        <Button 
          @click="itemsStore.fetchItems()"
          variant="default"
          size="lg"
          class="gap-2 shadow-lg shadow-indigo-100"
        >
          <RefreshCw :class="cn('w-4 h-4', itemsStore.loading && 'animate-spin')" />
          {{ itemsStore.loading ? 'Syncing...' : 'Refresh Catalog' }}
        </Button>
      </header>

      <div v-if="itemsStore.loading" class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card v-for="i in 6" :key="i" class="animate-pulse">
          <CardHeader class="pb-2">
            <div class="h-6 bg-gray-200 rounded w-2/3"></div>
          </CardHeader>
          <CardContent>
            <div class="h-4 bg-gray-100 rounded w-full mb-2"></div>
            <div class="h-4 bg-gray-100 rounded w-1/2"></div>
          </CardContent>
        </Card>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card 
          v-for="item in itemsStore.items" 
          :key="item.id"
          class="group hover:border-indigo-200 hover:shadow-md transition-all duration-300 cursor-pointer"
        >
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-lg font-bold group-hover:text-indigo-600 transition-colors">
              {{ item.name }}
            </CardTitle>
            <Box class="w-4 h-4 text-gray-400 group-hover:text-indigo-500" />
          </CardHeader>
          <CardContent>
            <p class="text-xs text-gray-400 font-mono uppercase tracking-widest mb-4">UID: {{ item.id }}</p>
            <div class="flex items-center gap-2 text-sm text-gray-600">
              <div class="w-2 h-2 rounded-full bg-green-500 shadow-sm shadow-green-200"></div>
              Active Resource
            </div>
          </CardContent>
        </Card>
      </div>
      
      <footer class="mt-16 pt-8 border-t border-gray-200 text-center text-gray-400 text-sm">
        <p>&copy; 2026 Vantage AI Modular Systems. Built with Vue 3, FastAPI, and Tailwind.</p>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useItemsStore } from '../store/itemsStore';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { RefreshCw, Package, Box } from 'lucide-vue-next';
import { cn } from '@/lib/utils';

const itemsStore = useItemsStore();

onMounted(() => {
  itemsStore.fetchItems();
});
</script>
