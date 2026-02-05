
import { wrap } from 'svelte-spa-router/wrap';
import { get } from 'svelte/store';
import { isAuthenticated } from '$lib/stores/auth';

export const protectedRoute = (component: any) =>
  wrap({
    component,
    conditions: [
      () => {
        if (!get(isAuthenticated)) {
          window.location.hash = '#/auth/login';
          return false;
        }
        return true;
      }
    ]
  });
