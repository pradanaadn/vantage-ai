import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || '/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface LoginResponse {
  uid: string;
  email: string;
  display_name: string | null;
  photo_url: string | null;
  email_verified: boolean;
  disabled: boolean;
}

export const authService = {
  async signup(email: string, password: string, displayName?: string) {
    const response = await api.post('/auth/signup', {
      email,
      password,
      display_name: displayName
    });
    return response.data;
  },

  async login(idToken: string) {
    const response = await api.post<LoginResponse>('/auth/login', {
      id_token: idToken
    });
    return response.data;
  }
};
