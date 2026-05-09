import { createRouter, createWebHistory } from 'vue-router';
import ItemsView from '@/modules/items/views/ItemsView.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: ItemsView,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
