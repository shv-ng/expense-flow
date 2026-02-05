<script lang="ts">
  import DashboardLayout from "$lib/components/DashboardLayout.svelte";
  import { Button } from "$lib/components/ui/button";
  import * as Card from "$lib/components/ui/card";
  import { Edit2, Trash2, Plus, Search, Tag } from "lucide-svelte";
  import { Input } from "$lib/components/ui/input";
  import AddCategoryDialog from "$lib/components/AddCategoryDialog.svelte";
  import { onMount } from "svelte";
import { categoriesApi, type Category } from "$lib/api/category";

let categories = $state<Category[]>([]);
  let searchQuery = $state(""); // Made this reactive state
  let loading = $state(true);
  let showAddDialog = $state(false);


  // WIRING: Fetch data from API
  async function loadCategories() {
    loading = true;
    try {
      categories = await categoriesApi.getAll();
    } catch (err) {
      console.error("Failed to load:", err);
    } finally {
      loading = false;
    }
  }

  // WIRING: Reactive filtering using Svelte 5 Runes
  let filteredCategories = $derived(
    categories.filter(cat => 
      cat.name.toLowerCase().includes(searchQuery.toLowerCase())
    )
  );

  onMount(loadCategories);

  // Placeholder for future delete wiring
  async function handleDeleteCategory(id: number) {
    if (confirm("Are you sure?")) {
        // await categoriesApi.delete(id);
        await loadCategories();
    }
  }
</script>

<AddCategoryDialog bind:open={showAddDialog} onSuccess={loadCategories} />

<DashboardLayout>
  <div class="space-y-8">
    <!-- Header -->
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h2 class="text-3xl font-bold tracking-tight">Categories</h2>
        <p class="text-muted-foreground mt-1">Organize and manage your expense categories</p>
      </div>
      <Button size="lg" class="gap-2" onclick={() => showAddDialog = true}>
        <Plus size={18} />
        Add Category
      </Button>
    </div>

    <!-- Search -->
    <div class="flex gap-4">
      <div class="relative flex-1 max-w-md">
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" size={18} />
        <Input 
          placeholder="Search categories..." 
          class="pl-10"
          bind:value={searchQuery}
        />
      </div>
    </div>

    {#if loading}
      <div class="flex items-center justify-center py-12">
        <p class="text-muted-foreground">Loading...</p>
      </div>
    {:else if filteredCategories.length === 0 && !searchQuery}
      <!-- Empty State -->
      <Card.Root>
        <Card.Content class="pt-12 pb-12">
          <div class="flex flex-col items-center justify-center text-center">
            <div class="rounded-full bg-muted p-6 mb-4">
              <Tag size={48} class="text-muted-foreground" />
            </div>
            <h3 class="text-xl font-semibold mb-2">No categories yet</h3>
            <p class="text-muted-foreground mb-6 max-w-sm">
              Start organizing your expenses by creating your first category
            </p>
            <Button size="lg" class="gap-2" onclick={() => showAddDialog = true}>
              <Plus size={18} />
              Create Your First Category
            </Button>
          </div>
        </Card.Content>
      </Card.Root>
    {:else if filteredCategories.length === 0}
      <!-- No Search Results -->
      <Card.Root>
        <Card.Content class="pt-12 pb-12">
          <div class="flex flex-col items-center justify-center text-center">
            <p class="text-muted-foreground">No categories found matching "{searchQuery}"</p>
          </div>
        </Card.Content>
      </Card.Root>
    {:else}
      <!-- Categories Grid -->
      <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {#each filteredCategories as category}
          <Card.Root class="group hover:shadow-xl hover:scale-[1.02] transition-all duration-200 cursor-pointer border-l-4" style="border-left-color: {category.color}">
            <Card.Content class="pt-6">
              <div class="flex items-start justify-between mb-4">
                <div class="flex items-center gap-3">
                  <div 
                    class="flex h-12 w-12 items-center justify-center rounded-xl"
                    style="background-color: {category.color}20"
                  >
                    <div class="h-5 w-5 rounded-full" style="background-color: {category.color}"></div>
                  </div>
                  <div>
                    <h3 class="font-semibold text-lg">{category.name}</h3>
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
