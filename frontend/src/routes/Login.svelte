<script lang="ts">
import { Button } from "$lib/components/ui/button";
import { Input } from "$lib/components/ui/input";
import * as Card from "$lib/components/ui/card";
import { Label } from "$lib/components/ui/label";
import { Mail, Lock } from "lucide-svelte";
import { login } from "$lib/api/auth";
import { setAuth } from "$lib/stores/auth";
import { push } from "svelte-spa-router";

let username = '';
let password = '';
let loading = false;
let error: string | null = null;

async function handleLogin() {
  loading = true;
  error = null;

  try {
    const res = await login(username, password);
    setAuth(res.access_token);
    push('/dashboard');
  } catch (err: any) {
    error = err?.detail ?? 'Login failed';
  } finally {
    loading = false;
  }
}
</script>

<div class="flex min-h-screen items-center justify-center bg-muted/50 p-4">
  <div class="w-full max-w-md space-y-6">
    <!-- Logo/Header -->
    <div class="text-center">
      <div class="inline-flex h-16 w-16 items-center justify-center rounded-2xl bg-primary/10 mb-4">
        <span class="text-3xl">💰</span>
      </div>
      <h1 class="text-3xl font-bold tracking-tight">Expense Tracker</h1>
      <p class="text-muted-foreground mt-2">Sign in to manage your expenses</p>
    </div>

    <Card.Root class="border-2">
      <Card.Header class="space-y-1">
        <Card.Title class="text-2xl">Welcome back</Card.Title>
        <Card.Description>Enter your credentials to access your account</Card.Description>
      </Card.Header>


      <form on:submit|preventDefault={handleLogin}>
        <Card.Content class="space-y-4">

          {#if error}
            <p class="text-sm text-destructive">{error}</p>
          {/if}
          <div class="space-y-2">
            <Label>Username</Label>
            <div class="relative">
              <Mail class="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" size={18} />
              <Input
                bind:value={username}
                type="text"
                placeholder="johndoe"
                class="pl-10"
                autocomplete="username"
                required
              />
            </div>
          </div>

          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <Label>Password</Label>
            </div>
            <div class="relative">
              <Lock class="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" size={18} />
              <Input
                bind:value={password}
                type="password"
                placeholder="••••••••"
                class="pl-10"
                autocomplete="current-password"
                required
              />
            </div>
          </div>

        </Card.Content>

        <Card.Footer class="flex-col gap-3">
          <Button
            class="w-full"
            size="lg"
            type="submit"
            disabled={loading}
          >
            {loading ? 'Signing in…' : 'Sign in'}
          </Button>

          <div class="relative w-full">
            <div class="absolute inset-0 flex items-center">
              <span class="w-full border-t"></span>
            </div>
            <div class="relative flex justify-center text-xs uppercase">
              <span class="bg-card px-2 text-muted-foreground">Or</span>
            </div>
          </div>

          <div class="text-center text-sm">
            <span class="text-muted-foreground">Don't have an account?</span>
            {' '}
            <a href="#/auth/register" class="text-primary font-semibold hover:underline">
              Create account
            </a>
          </div>
        </Card.Footer>
      </form>
    </Card.Root>

  </div>
</div>
