<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { 
    LayoutDashboard, 
    Tag, 
    Receipt, 
    TrendingUp, 
    LogOut,
    Menu,
    X,
    User
  } from "lucide-svelte";
  import { logout } from "$lib/stores/auth";
  import { usersApi, type UserProfile } from "$lib/api/users";
  import { onMount } from "svelte";
  
  const navItems = [
    { href: "#/dashboard", label: "Dashboard", icon: LayoutDashboard },
    { href: "#/categories", label: "Categories", icon: Tag },
    { href: "#/expenses", label: "Expenses", icon: Receipt },
    { href: "#/analytics", label: "Analytics", icon: TrendingUp },
  ];

  let sidebarOpen = $state(true);
  let currentPath = $state(window.location.hash || "#/dashboard");
  let userProfile = $state<UserProfile | null>(null);

  const toggleSidebar = () => {
    sidebarOpen = !sidebarOpen;
  };

  // Update current path on navigation
  window.addEventListener('hashchange', () => {
    currentPath = window.location.hash;
  });

  const isActive = (href: string) => {
    return currentPath === href || (href === "#/dashboard" && currentPath === "#/");
  };

  // Load user profile
  onMount(async () => {
    try {
      userProfile = await usersApi.getProfile();
    } catch (err) {
      console.error("Failed to load user profile:", err);
    }
  });

  function handleLogout() {
    logout();
    window.location.hash = "#/auth/login";
  }
</script>

<div class="flex min-h-screen bg-muted/30">
  <!-- Sidebar -->
  <aside 
    class="fixed left-0 top-0 z-40 h-screen w-64 border-r bg-card transition-transform duration-300 ease-in-out lg:translate-x-0"
    class:translate-x-0={sidebarOpen}
    class:-translate-x-full={!sidebarOpen}
  >
    <div class="flex h-full flex-col">
      <!-- Logo -->
      <div class="flex h-16 items-center gap-3 border-b px-6">
        <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
          <span class="text-xl">💰</span>
        </div>
        <div>
          <h2 class="text-lg font-bold">Expense Tracker</h2>
          <p class="text-xs text-muted-foreground">Manage your finances</p>
        </div>
      </div>
      
      <!-- Navigation -->
      <nav class="flex-1 space-y-1 p-4">
        {#each navItems as item}
          <a
            href={item.href}
            class="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all hover:bg-accent hover:text-accent-foreground"
            class:bg-primary={isActive(item.href)}
            class:text-primary-foreground={isActive(item.href)}
            class:hover:bg-primary90={isActive(item.href)}
          >
            <svelte:component this={item.icon} size={20} />
            {item.label}
          </a>
        {/each}
      </nav>

      <!-- User Profile -->
      <div class="border-t p-4">
        <div class="flex items-center gap-3 rounded-lg p-2 hover:bg-accent transition-colors cursor-pointer">
          <div class="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
            <User size={20} class="text-primary" />
          </div>
          <div class="flex-1 min-w-0">
            {#if userProfile}
              <p class="text-sm font-semibold truncate">
                {userProfile.full_name || userProfile.username}
              </p>
              <p class="text-xs text-muted-foreground truncate">{userProfile.email}</p>
            {:else}
              <p class="text-sm font-semibold truncate">Loading...</p>
            {/if}
          </div>
        </div>
        <Button 
          variant="ghost" 
          class="w-full justify-start gap-2 mt-2"
          size="sm"
          onclick={handleLogout}
        >
          <LogOut size={16} />
          Logout
        </Button>
      </div>
    </div>
  </aside>

  <!-- Main Content -->
  <div 
    class="flex-1 transition-all duration-300"
    class:lg:ml-64={true}
  >
    <!-- Header -->
    <header class="sticky top-0 z-30 border-b bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/60">
      <div class="flex h-16 items-center gap-4 px-6">
        <Button 
          variant="ghost" 
          size="icon" 
          class="lg:hidden"
          onclick={toggleSidebar}
        >
          {#if sidebarOpen}
            <X size={20} />
          {:else}
            <Menu size={20} />
          {/if}
        </Button>

        <div class="flex-1"></div>
      </div>
    </header>

    <!-- Content Area -->
    <main class="p-6 lg:p-8">
      <slot />
    </main>

    <!-- Footer -->
    <footer class="border-t bg-card py-6 px-6 lg:px-8">
      <div class="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <p class="text-sm text-muted-foreground">
          © 2026 Expense Tracker. All rights reserved.
        </p>
        <div class="flex gap-4 text-sm">
          <a href="#" class="text-muted-foreground hover:text-foreground transition-colors">
            Privacy
          </a>
          <a href="#" class="text-muted-foreground hover:text-foreground transition-colors">
            Terms
          </a>
          <a href="#" class="text-muted-foreground hover:text-foreground transition-colors">
            Help
          </a>
        </div>
      </div>
    </footer>
  </div>
</div>

<!-- Mobile Overlay -->
{#if sidebarOpen}
  <div 
    class="fixed inset-0 z-30 bg-background/80 backdrop-blur-sm lg:hidden"
    onclick={toggleSidebar}
  ></div>
{/if}
