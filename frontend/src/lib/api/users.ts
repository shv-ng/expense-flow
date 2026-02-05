import { api } from './client';

export interface UserProfile {
  username: string;
  email: string;
  full_name: string | null;
}

export const usersApi = {
  getProfile: () => api<UserProfile>('/users/'),
};
