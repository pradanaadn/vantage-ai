import { createRouter, createWebHistory } from 'vue-router';

// Modular route definitions could be imported here
// e.g., import { itemRoutes } from '@/modules/items/router';

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/modules/items/views/ItemsView.vue'),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
