// frontend/src/lib/api/category.ts
import { api } from './client';

export interface Category {
  id: number;
  name: string;
  color: string;
}

export const categoriesApi = {
  getAll: () => api<Category[]>('/categories/'),
  create: (name: string, color: string) => 
    api<Category>('/categories/', {
      method: 'POST',
      body: { name, color },
    })
};
