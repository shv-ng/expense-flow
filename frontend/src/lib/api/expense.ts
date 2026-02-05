import { api } from './client';

export interface Expense {
  id: string;
  amount: number;
  description: string;
  date: string;
  category_id: string;
  category?: {
    name: string;
    color: string;
  };
}

export const expensesApi = {
  getAll: (filters: { date_from?: string; date_to?: string; category_id?: string }) => {
    const params = new URLSearchParams();
    if (filters.date_from) params.append('date_from', filters.date_from);
    if (filters.date_to) params.append('date_to', filters.date_to);
    if (filters.category_id) params.append('category_id', filters.category_id);
    
    return api<Expense[]>(`/expenses/?${params.toString()}`);
  },
  
  create: (data: { amount: number; category_id: string; date: string; description?: string }) =>
    api<Expense>('/expenses/', {
      method: 'POST',
      body: data,
    }),

  delete: (id: string) => 
    api(`/expenses/${id}`, { method: 'DELETE' })
};
