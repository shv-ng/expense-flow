<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import * as Card from "$lib/components/ui/card";
  import { Label } from "$lib/components/ui/label";
  import { User, Mail, Lock } from "lucide-svelte";
  import { register } from "$lib/api/auth";
  import { push } from "svelte-spa-router";

  let username = '';
  let email = '';
  let password = '';

  let loading = false;
  let error: string | null = null;

  async function handleRegister() {
    error = null;
    loading = true;
    if (!username || !email || !password ) {
      error = 'Please fill in all fields';
      loading = false;
      return;
    }
    if (password.length < 8) {
      error = 'Password must be at least 8 characters long';
      loading = false;
      return;
    }

    try {
      await register(username, email, password);
      push('/auth/login');
    } catch (err: any) {
      console.error(err);
      error = err?.detail?.[0]?.msg ?? 'Registration failed';
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
      <p class="text-muted-foreground mt-2">Create your account to get started</p>
    </div>

    <Card.Root class="border-2">
      <Card.Header class="space-y-1">
        <Card.Title class="text-2xl">Create account</Card.Title>
        <Card.Description>Enter your details to register</Card.Description>
      </Card.Header>
<form on:submit|preventDefault={handleRegister}>
      <Card.Content class="space-y-4">
        {#if error}
          <p class="text-sm text-destructive">{error}</p>
        {/if}
        <div class="space-y-2">
          <Label>Username</Label>
          <div class="relative">
            <User class="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" size={18} />
            <Input 
              type="text"
              placeholder="johndoe" 
              class="pl-10"
              bind:value={username}
            />
          </div>
        </div>

        <div class="space-y-2">
          <Label>Email</Label>
          <div class="relative">
            <Mail class="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" size={18} />
            <Input 
              type="email"
              placeholder="john@example.com" 
              class="pl-10"
              bind:value={email}
            />
          </div>
        </div>

        <div class="space-y-2">
          <Label>Password</Label>
          <div class="relative">
            <Lock class="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" size={18} />
            <Input 
              type="password" 
              placeholder="••••••••"
              class="pl-10"
              bind:value={password}
            />
          </div>
          <p class="text-xs text-muted-foreground">
            Must be at least 8 characters with a mix of letters and numbers
          </p>
        </div>

      </Card.Content>

      <Card.Footer class="flex-col gap-3">
<Button
      class="w-full"
      size="lg"
      type="submit"
      disabled={loading}
    >
      {loading ? 'Creating account…' : 'Create account'}
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
          <span class="text-muted-foreground">Already have an account?</span>
          {' '}
          <a href="#/auth/login" class="text-primary font-semibold hover:underline">
            Sign in
          </a>
        </div>
      </Card.Footer>
        </form>
    </Card.Root>

  </div>
</div>
