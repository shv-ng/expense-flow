<script lang='ts'>
  import Router from 'svelte-spa-router';
  import Login from './routes/Login.svelte';
  import Register from './routes/Register.svelte';
  import Dashboard from './routes/Dashboard.svelte';
  import Categories from './routes/Categories.svelte';
  import Expenses from './routes/Expenses.svelte';
  import Analytics from './routes/Analytics.svelte';
  import NotFound from './routes/NotFound.svelte';

  import { protectedRoute } from './router/guards';
</script>

<Router routes={{
  '/auth/login': Login,
  '/auth/register': Register,

  '/': protectedRoute(Dashboard),
  '/dashboard': protectedRoute(Dashboard),
  '/categories': protectedRoute(Categories),
  '/expenses': protectedRoute(Expenses),
  '/analytics': protectedRoute(Analytics),

  "*": NotFound
}} />
