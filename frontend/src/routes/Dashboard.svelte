<script lang="ts">
  import DashboardLayout from "$lib/components/DashboardLayout.svelte";
  import * as Card from "$lib/components/ui/card";
  import { Button } from "$lib/components/ui/button";
  import { TrendingUp, TrendingDown, DollarSign, Tag, Receipt } from "lucide-svelte";
  import AddExpenseDialog from "$lib/components/AddExpenseDialog.svelte";
  import { onMount } from "svelte";
  import { expensesApi, type Expense } from "$lib/api/expense";
  import { categoriesApi, type Category } from "$lib/api/category";

  let stats = $state({
    totalSpent: 0,
    categoriesCount: 0,
    transactionsCount: 0
  });

  let recentExpenses = $state<Expense[]>([]);
  let categories = $state<Category[]>([]);
  let showAddExpenseDialog = $state(false);
  let loading = $state(true);

  onMount(async () => {
    await loadData();
  });

  async function loadData() {
    loading = true;
    try {
      const [expensesRes, categoriesRes] = await Promise.all([
        expensesApi.getAll({}),
        categoriesApi.getAll()
      ]);

      // Calculate stats
      stats.totalSpent = expensesRes.reduce((sum, exp) => sum + exp.amount, 0);
      stats.categoriesCount = categoriesRes.length;
      stats.transactionsCount = expensesRes.length;

      // Get recent expenses (last 5)
      recentExpenses = expensesRes
        .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
        .slice(0, 5);

      categories = categoriesRes.slice(0, 5);
    } catch (err) {
      console.error("Failed to load dashboard data:", err);
    } finally {
      loading = false;
    }
  }
</script>

<AddExpenseDialog bind:open={showAddExpenseDialog} onSuccess={loadData} />

<DashboardLayout>
  <div class="space-y-8">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-3xl font-bold tracking-tight">Dashboard</h2>
        <p class="text-muted-foreground mt-1">Overview of your expenses and spending habits</p>
      </div>
      <Button size="lg" class="gap-2" onclick={() => showAddExpenseDialog = true}>
        <span class="text-lg">+</span>
        Add Expense
      </Button>
    </div>

    {#if loading}
      <div class="flex items-center justify-center py-12">
        <p class="text-muted-foreground">Loading dashboard...</p>
      </div>
    {:else}
      <!-- Stats Cards -->
      <div class="grid gap-6 md:grid-cols-3">
        <Card.Root class="border-l-4" style="border-left-color: #3b82f6">
          <Card.Content class="pt-6">
            <div class="flex items-start justify-between">
              <div class="space-y-2">
                <p class="text-sm font-medium text-muted-foreground">Total Spent</p>
                <p class="text-3xl font-bold tracking-tight">${stats.totalSpent.toFixed(2)}</p>
              </div>
              <div class="rounded-lg bg-muted/50 p-3">
                <DollarSign class="text-blue-600" size={24} />
              </div>
            </div>
          </Card.Content>
        </Card.Root>

        <Card.Root class="border-l-4" style="border-left-color: #a855f7">
          <Card.Content class="pt-6">
            <div class="flex items-start justify-between">
              <div class="space-y-2">
                <p class="text-sm font-medium text-muted-foreground">Categories</p>
                <p class="text-3xl font-bold tracking-tight">{stats.categoriesCount}</p>
              </div>
              <div class="rounded-lg bg-muted/50 p-3">
                <Tag class="text-purple-600" size={24} />
              </div>
            </div>
          </Card.Content>
        </Card.Root>

        <Card.Root class="border-l-4" style="border-left-color: #10b981">
          <Card.Content class="pt-6">
            <div class="flex items-start justify-between">
              <div class="space-y-2">
                <p class="text-sm font-medium text-muted-foreground">Transactions</p>
                <p class="text-3xl font-bold tracking-tight">{stats.transactionsCount}</p>
              </div>
              <div class="rounded-lg bg-muted/50 p-3">
                <Receipt class="text-emerald-600" size={24} />
              </div>
            </div>
          </Card.Content>
        </Card.Root>
      </div>

      <div class="grid gap-6 lg:grid-cols-3">
        <!-- Recent Expenses -->
        <div class="lg:col-span-2">
          <Card.Root>
            <Card.Header>
              <div class="flex items-center justify-between">
                <div>
                  <Card.Title class="text-xl">Recent Expenses</Card.Title>
                  <Card.Description class="mt-1">Your latest transactions</Card.Description>
                </div>
                <Button variant="ghost" size="sm" onclick={() => window.location.hash = "#/expenses"}>
                  View all
                </Button>
              </div>
            </Card.Header>
            <Card.Content>
              {#if recentExpenses.length === 0}
                <div class="flex flex-col items-center justify-center py-12 text-center">
                  <div class="rounded-full bg-muted p-4 mb-4">
                    <Receipt size={32} class="text-muted-foreground" />
                  </div>
                  <p class="text-lg font-semibold mb-2">No expenses yet</p>
                  <p class="text-sm text-muted-foreground mb-4">Start tracking your expenses by adding one</p>
                  <Button size="sm" class="gap-2" onclick={() => showAddExpenseDialog = true}>
                    <span>+</span>
                    Add Your First Expense
                  </Button>
                </div>
              {:else}
                <div class="space-y-1">
                  {#each recentExpenses as expense, index}
                    <div class="group flex items-center gap-4 rounded-lg p-3 hover:bg-muted/50 transition-colors">
                      <div class="flex h-10 w-10 items-center justify-center rounded-full" style="background-color: {expense.category?.color}20">
                        <div class="h-4 w-4 rounded-full" style="background-color: {expense.category?.color || '#666'}"></div>
                      </div>
                      <div class="flex-1 min-w-0">
                        <p class="font-medium text-sm truncate">{expense.description || 'No description'}</p>
                        <div class="flex items-center gap-2 text-xs text-muted-foreground mt-0.5">
                          <span class="font-medium">{expense.category?.name || 'Uncategorized'}</span>
                          <span>•</span>
                          <span>{new Date(expense.date).toLocaleDateString()}</span>
                        </div>
                      </div>
                      <span class="text-lg font-bold tabular-nums">${expense.amount.toFixed(2)}</span>
                    </div>
                    {#if index < recentExpenses.length - 1}
                      <div class="h-px bg-border mx-3"></div>
                    {/if}
                  {/each}
                </div>
              {/if}
            </Card.Content>
          </Card.Root>
        </div>

        <!-- Categories -->
        <div class="lg:col-span-1">
          <Card.Root>
            <Card.Header>
              <div class="flex items-center justify-between">
                <div>
                  <Card.Title class="text-xl">Categories</Card.Title>
                  <Card.Description class="mt-1">Your expense categories</Card.Description>
                </div>
                <Button variant="ghost" size="sm" onclick={() => window.location.hash = "#/categories"}>
                  View all
                </Button>
              </div>
            </Card.Header>
            <Card.Content>
              {#if categories.length === 0}
                <div class="flex flex-col items-center justify-center py-8 text-center">
                  <div class="rounded-full bg-muted p-3 mb-3">
                    <Tag size={24} class="text-muted-foreground" />
                  </div>
                  <p class="text-sm font-semibold mb-1">No categories yet</p>
                  <p class="text-xs text-muted-foreground mb-3">Create categories to organize your expenses</p>
                  <Button size="sm" variant="outline" onclick={() => window.location.hash = "#/categories"}>
                    Add Category
                  </Button>
                </div>
              {:else}
                <div class="space-y-3">
                  {#each categories as category}
                    <div class="flex items-center gap-3 p-2 rounded-lg hover:bg-muted/50 transition-colors cursor-pointer">
                      <div class="h-8 w-8 rounded-lg flex items-center justify-center" style="background-color: {category.color}20">
                        <div class="h-3 w-3 rounded-full" style="background-color: {category.color}"></div>
                      </div>
                      <span class="font-medium text-sm flex-1">{category.name}</span>
                    </div>
                  {/each}
                </div>
              {/if}
            </Card.Content>
          </Card.Root>
        </div>
      </div>
    {/if}
  </div>
</DashboardLayout>
