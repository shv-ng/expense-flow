import { api } from './client';

export interface SpendingByDate {
  labels: string[];
  data: number[];
}

export interface SpendingByCategory {
  labels: string[];
  data: number[];
}

export interface SpendingByMonth {
  labels: number[];
  data: number[];
}

export const analyticsApi = {
  getSpendingByDate: () => 
    api<SpendingByDate>('/analytics/spending-by-date'),
  
  getSpendingByCategory: () => 
    api<SpendingByCategory>('/analytics/spending-by-category'),
  
  getSpendingByMonth: () => 
    api<SpendingByMonth>('/analytics/spending-by-month'),
};
