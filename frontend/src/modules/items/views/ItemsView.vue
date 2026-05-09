<template>
  <div class="min-h-screen bg-muted/30 p-8 text-foreground">
    <div class="max-w-5xl mx-auto">
      <header class="mb-10 flex flex-col md:flex-row justify-between items-start md:items-end gap-6">
        <div>
          <div class="flex items-center gap-2 mb-3">
            <div class="p-2 bg-primary rounded-lg shadow-primary/20 shadow-lg">
              <Package class="w-5 h-5 text-primary-foreground" />
            </div>
            <span class="text-[10px] font-bold text-primary uppercase tracking-[0.3em]">Cloud Infrastructure</span>
          </div>
          <h1 class="text-4xl font-extrabold tracking-tight">Resource Catalog</h1>
          <p class="text-muted-foreground mt-2 text-lg font-medium">Simplified asset orchestration and monitoring.</p>
        </div>
        
        <Button 
          @click="loadItems"
          variant="default"
          size="lg"
          class="gap-2 shadow-lg shadow-primary/10"
          :disabled="loading"
        >
          <RefreshCw :class="cn('w-4 h-4', loading && 'animate-spin')" />
          {{ loading ? 'Syncing...' : 'Refresh Data' }}
        </Button>
      </header>

      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card v-for="i in 6" :key="i" class="animate-pulse bg-card border-border">
          <CardHeader class="pb-2">
            <div class="h-6 bg-muted rounded w-2/3"></div>
          </CardHeader>
          <CardContent>
            <div class="h-4 bg-muted/50 rounded w-full mb-2"></div>
            <div class="h-4 bg-muted/50 rounded w-1/2"></div>
          </CardContent>
        </Card>
      </div>

      <div v-else-if="error" class="bg-destructive/10 border border-destructive/20 p-6 rounded-xl text-destructive text-center">
        <p class="font-semibold">{{ error }}</p>
        <Button variant="outline" class="mt-4" @click="loadItems">Try Again</Button>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card 
          v-for="item in items" 
          :key="item.id"
          class="group bg-card border-border hover:border-primary/30 hover:shadow-md transition-all duration-300 cursor-pointer"
        >
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-lg font-bold group-hover:text-primary transition-colors">
              {{ item.name }}
            </CardTitle>
            <Box class="w-4 h-4 text-muted-foreground group-hover:text-primary/70" />
          </CardHeader>
          <CardContent>
            <p class="text-[10px] text-muted-foreground font-mono uppercase tracking-widest mb-4">UUID: {{ item.id }}</p>
            <div class="flex items-center gap-2 text-sm font-semibold text-muted-foreground">
              <div class="w-2 h-2 rounded-full bg-primary shadow-sm shadow-primary/30"></div>
              Active
            </div>
          </CardContent>
        </Card>
      </div>
      
      <footer class="mt-20 pt-8 border-t border-border text-center text-muted-foreground text-xs uppercase tracking-widest">
        <p>&copy; 2026 Vantage AI Modular Systems. Simplified Edition.</p>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { itemsService } from '@/services/items';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { RefreshCw, Package, Box } from 'lucide-vue-next';
import { cn } from '@/lib/utils';

const items = ref<any[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

const loadItems = async () => {
  loading.value = true;
  error.value = null;
  try {
    items.value = await itemsService.fetchAll();
  } catch (e) {
    error.value = 'Failed to load catalog. Please check your connection.';
  } finally {
    loading.value = false;
  }
};

onMounted(loadItems);
</script>
