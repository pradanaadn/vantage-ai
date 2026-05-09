const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost/api/v1';

export const itemsService = {
  async fetchAll() {
    const response = await fetch(`${API_BASE_URL}/items`);
    if (!response.ok) throw new Error('Failed to fetch items');
    return response.json();
  }
};
