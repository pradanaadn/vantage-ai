import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

interface User {
  uid: string;
  email: string | null;
  display_name?: string | null;
  photo_url?: string | null;
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const isAuthenticated = computed(() => !!user.value);

  function setUser(newUser: User | null) {
    user.value = newUser;
  }

  function setLoading(val: boolean) {
    loading.value = val;
  }

  function setError(msg: string | null) {
    error.value = msg;
  }

  return {
    user,
    loading,
    error,
    isAuthenticated,
    setUser,
    setLoading,
    setError
  };
});
