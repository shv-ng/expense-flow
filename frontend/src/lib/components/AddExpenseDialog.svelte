<script lang="ts">
  import * as Dialog from "$lib/components/ui/dialog";
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Label } from "$lib/components/ui/label";
  import { onMount } from "svelte";
  import { expensesApi } from "$lib/api/expense";
  import { categoriesApi } from "$lib/api/category";

  let { open = $bindable(false), onSuccess }: { open?: boolean; onSuccess?: () => void } = $props();

  let amount = $state("");
  let description = $state("");
  let categoryId = $state("");
  let date = $state(new Date().toISOString().split('T')[0]);
  let categories = $state<any[]>([]);
  let loading = $state(false);
  let error = $state("");

  // Fetch categories when component mounts so the dropdown works
  onMount(async () => {
    try {
      categories = await categoriesApi.getAll();
    } catch (err) {
      console.error("Failed to load categories:", err);
    }
  });

  async function handleSubmit() {
    error = "";
    if (!amount || parseFloat(amount) <= 0) { error = "Please enter a valid amount"; return; }
    if (!categoryId) { error = "Please select a category"; return; }

    loading = true;
    try {
      await expensesApi.create({
        amount: parseFloat(amount),
        category_id: categoryId,
        date: date,
        description: description.trim() || undefined,
      });
      
      open = false;
      resetForm();
      onSuccess?.(); // This triggers loadData in the parent
    } catch (err: any) {
      error = err.message || "Failed to create expense";
    } finally {
      loading = false;
    }
  }

  function resetForm() {
    amount = "";
    description = "";
    categoryId = "";
    date = new Date().toISOString().split('T')[0];
    error = "";
  }

  function handleOpenChange(isOpen: boolean) {
    open = isOpen;
    if (!isOpen) {
      resetForm();
    }
  }
</script>

<Dialog.Root bind:open onOpenChange={handleOpenChange}>
  <Dialog.Content class="sm:max-w-[500px]">
    <Dialog.Header>
      <Dialog.Title>Add Expense</Dialog.Title>
      <Dialog.Description>
        Record a new expense to track your spending
      </Dialog.Description>
    </Dialog.Header>

    <div class="grid gap-4 py-4">
      <div class="grid grid-cols-2 gap-4">
        <div class="space-y-2">
          <Label for="amount">Amount *</Label>
          <div class="relative">
            <span class="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground">$</span>
            <Input
              id="amount"
              type="number"
              step="0.01"
              min="0"
              placeholder="0.00"
              bind:value={amount}
              disabled={loading}
              class="pl-7"
            />
          </div>
        </div>

        <div class="space-y-2">
          <Label for="date">Date *</Label>
          <Input
            id="date"
            type="date"
            bind:value={date}
            disabled={loading}
          />
        </div>
      </div>

      <div class="space-y-2">
        <Label for="category">Category *</Label>
        <select
          id="category"
          bind:value={categoryId}
          disabled={loading || categories.length === 0}
          class="flex h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-sm shadow-xs transition-colors hover:border-ring focus:outline-none focus:ring-1 focus:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
        >
          <option value="">Select a category</option>
          {#each categories as category}
            <option value={category.id}>{category.name}</option>
          {/each}
        </select>
        {#if categories.length === 0}
          <p class="text-xs text-muted-foreground">
            No categories available. Create one first!
          </p>
        {/if}
      </div>

      <div class="space-y-2">
        <Label for="description">Description (optional)</Label>
        <Input
          id="description"
          placeholder="e.g., Weekly groceries at Walmart"
          bind:value={description}
          disabled={loading}
        />
      </div>

      {#if error}
        <div class="rounded-md bg-destructive/10 p-3 text-sm text-destructive">
          {error}
        </div>
      {/if}
    </div>

    <Dialog.Footer>
      <Button variant="outline" onclick={() => open = false} disabled={loading}>
        Cancel
      </Button>
      <Button onclick={handleSubmit} disabled={loading || categories.length === 0}>
        {loading ? "Adding..." : "Add Expense"}
      </Button>
    </Dialog.Footer>
  </Dialog.Content>
</Dialog.Root>
