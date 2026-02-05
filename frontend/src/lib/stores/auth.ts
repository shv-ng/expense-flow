import { writable } from 'svelte/store';

const STORAGE_KEY = 'expense-tracker-token';

const storedToken =
  typeof localStorage !== 'undefined'
    ? localStorage.getItem(STORAGE_KEY)
    : null;

export const token = writable<string | null>(storedToken);
export const isAuthenticated = writable<boolean>(!!storedToken);

export function setAuth(accessToken: string) {
  token.set(accessToken);
  isAuthenticated.set(true);
  localStorage.setItem(STORAGE_KEY, accessToken);
}

export function logout() {
  token.set(null);
  isAuthenticated.set(false);
  localStorage.removeItem(STORAGE_KEY);
}
