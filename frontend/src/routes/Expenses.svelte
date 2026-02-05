<script lang="ts">
  import DashboardLayout from "$lib/components/DashboardLayout.svelte";
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import * as Card from "$lib/components/ui/card";
  import { Label } from "$lib/components/ui/label";
  import { Plus, Filter, Download, Edit2, Trash2, Calendar, DollarSign, Receipt } from "lucide-svelte";
  import AddExpenseDialog from "$lib/components/AddExpenseDialog.svelte";
  import { onMount } from "svelte";
import { expensesApi, type Expense } from "$lib/api/expense";
  import { categoriesApi } from "$lib/api/category";

let expenses = $state<Expense[]>([]);
  let categories = $state<any[]>([]);
  let loading = $state(true);
  let showAddDialog = $state(false);

  // Filters
let dateFrom = $state("");
  let dateTo = $state("");
  let selectedCategoryId = $state("");


let totalAmount = $derived(expenses.reduce((sum, exp) => sum + exp.amount, 0));
  let averageExpense = $derived(expenses.length > 0 ? totalAmount / expenses.length : 0);

async function loadData() {
    loading = true;
    try {
      // Fetch both in parallel
      const [expensesRes, categoriesRes] = await Promise.all([
        expensesApi.getAll({ 
          date_from: dateFrom || undefined, 
          date_to: dateTo || undefined, 
          category_id: selectedCategoryId || undefined 
        }),
        categoriesApi.getAll()
      ]);
      
      expenses = expensesRes;
      categories = categoriesRes;
    } catch (err) {
      console.error(err);
    } finally {
      loading = false;
    }
  }

  // Triggered by filter changes
  function handleFilterChange() {
    loadData();
  }

  async function handleDeleteExpense(id: string) {
    if (!confirm("Are you sure you want to delete this expense?")) return;
    try {
      await expensesApi.delete(id);
      await loadData(); // Refresh list
    } catch (err) {
      alert("Failed to delete");
    }
  }

  function clearFilters() {
    dateFrom = '';
    dateTo = '';
    selectedCategoryId = '';
    loadData();
  }

  onMount(loadData);
</script>

<AddExpenseDialog bind:open={showAddDialog} onSuccess={loadData} />

<DashboardLayout>
  <div class="space-y-8">
    <!-- Header -->
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h2 class="text-3xl font-bold tracking-tight">Expenses</h2>
        <p class="text-muted-foreground mt-1">Track and manage all your expenses</p>
      </div>
      <div class="flex gap-3">
        <Button size="lg" class="gap-2" onclick={() => showAddDialog = true}>
          <Plus size={18} />
          Add Expense
        </Button>
      </div>
    </div>

    <!-- Summary Cards -->
    <div class="grid gap-4 sm:grid-cols-3">
      <Card.Root>
        <Card.Content class="pt-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-muted-foreground">Total Expenses</p>
              <p class="text-2xl font-bold mt-1">${totalAmount.toFixed(2)}</p>
            </div>
            <div class="rounded-lg bg-primary/10 p-3">
              <DollarSign class="text-primary" size={22} />
            </div>
          </div>
        </Card.Content>
      </Card.Root>

      <Card.Root>
        <Card.Content class="pt-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-muted-foreground">Transactions</p>
              <p class="text-2xl font-bold mt-1">{expenses.length}</p>
            </div>
            <div class="rounded-lg bg-emerald-500/10 p-3">
              <span class="text-xl">📝</span>
            </div>
          </div>
        </Card.Content>
      </Card.Root>

      <Card.Root>
        <Card.Content class="pt-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-muted-foreground">Average</p>
              <p class="text-2xl font-bold mt-1">
                ${expenses.length > 0 ? (totalAmount / expenses.length).toFixed(2) : '0.00'}
              </p>
            </div>
            <div class="rounded-lg bg-blue-500/10 p-3">
              <span class="text-xl">📊</span>
            </div>
          </div>
        </Card.Content>
      </Card.Root>
    </div>

    <!-- Filters -->
    <Card.Root>
      <Card.Header>
        <div class="flex items-center gap-2">
          <Filter size={18} class="text-muted-foreground" />
          <Card.Title>Filters</Card.Title>
        </div>
      </Card.Header>
      <Card.Content>
        <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <div class="space-y-2">
            <Label>From Date</Label>
            <Input type="date" bind:value={dateFrom} onchange={handleFilterChange} />
          </div>
          <div class="space-y-2">
            <Label>To Date</Label>
            <Input type="date" bind:value={dateTo} onchange={handleFilterChange} />
          </div>
          <div class="space-y-2">
            <Label>Category</Label>
            <select 
              class="flex h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-sm shadow-xs transition-colors hover:border-ring"
              bind:value={selectedCategoryId}
              onchange={handleFilterChange}
            >
              <option value="">All Categories</option>
              {#each categories as category}
                <option value={category.id}>{category.name}</option>
              {/each}
            </select>
          </div>
          <div class="space-y-2 flex items-end">
            <Button variant="outline" class="w-full" onclick={clearFilters}>
              Clear Filters
            </Button>
          </div>
        </div>
      </Card.Content>
    </Card.Root>

    {#if loading}
      <div class="flex items-center justify-center py-12">
        <p class="text-muted-foreground">Loading...</p>
      </div>
    {:else if expenses.length === 0}
      <!-- Empty State -->
      <Card.Root>
        <Card.Content class="pt-12 pb-12">
          <div class="flex flex-col items-center justify-center text-center">
            <div class="rounded-full bg-muted p-6 mb-4">
              <Receipt size={48} class="text-muted-foreground" />
            </div>
            <h3 class="text-xl font-semibold mb-2">No expenses yet</h3>
            <p class="text-muted-foreground mb-6 max-w-sm">
              Start tracking your spending by adding your first expense
            </p>
            <Button size="lg" class="gap-2" onclick={() => showAddDialog = true}>
              <Plus size={18} />
              Add Your First Expense
            </Button>
          </div>
        </Card.Content>
      </Card.Root>
    {:else}
      <!-- Expenses List -->
      <div class="space-y-4">
        {#each expenses as expense}
          <Card.Root class="group hover:shadow-lg transition-all duration-200">
            <Card.Content class="pt-6">
              <div class="flex items-center gap-4">
                <!-- Category Icon -->
                <div 
                  class="flex h-14 w-14 shrink-0 items-center justify-center rounded-xl"
                  style="background-color: {expense.category?.color}20"
                >
                  <div class="h-6 w-6 rounded-full" style="background-color: {expense.category?.color || '#666'}"></div>
                </div>

                <!-- Expense Details -->
                <div class="flex-1 min-w-0">
                  <div class="flex items-start justify-between gap-4">
                    <div class="flex-1 min-w-0">
                      <h3 class="font-semibold text-base truncate">{expense.description || 'No description'}</h3>
                      <div class="flex flex-wrap items-center gap-2 mt-1.5 text-sm text-muted-foreground">
                        <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md font-medium" style="background-color: {expense.category?.color}20; color: {expense.category?.color}">
                          {expense.category?.name || 'Uncategorized'}
                        </span>
                        <span class="hidden sm:inline">•</span>
                        <span class="hidden sm:inline flex items-center gap-1">
                          <Calendar size={14} />
                          {new Date(expense.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                        </span>
                      </div>
                    </div>

                    <!-- Amount and Actions -->
                    <div class="flex items-center gap-4 shrink-0">
                      <span class="text-2xl font-bold tabular-nums">${expense.amount.toFixed(2)}</span>
                      <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <Button variant="ghost" size="icon-sm" class="h-8 w-8" onclick={() => handleEditExpense(expense.id)}>
                          <Edit2 size={16} />
                        </Button>
                        <Button variant="ghost" size="icon-sm" class="h-8 w-8 hover:bg-destructive/10 hover:text-destructive" onclick={() => handleDeleteExpense(expense.id)}>
                          <Trash2 size={16} />
                        </Button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </Card.Content>
          </Card.Root>
        {/each}
      </div>
    {/if}
  </div>
</DashboardLayout>
