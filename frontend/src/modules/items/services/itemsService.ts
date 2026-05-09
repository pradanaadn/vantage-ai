import api from '@/services/api';

export const itemsService = {
  async getItems() {
    const response = await api.get('/items');
    return response.data;
  },
};
