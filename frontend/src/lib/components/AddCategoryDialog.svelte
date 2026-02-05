<script lang="ts">
  import * as Dialog from "$lib/components/ui/dialog";
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Label } from "$lib/components/ui/label";
  import { categoriesApi } from "$lib/api/category";

  let { open = $bindable(false), onSuccess }: { open?: boolean; onSuccess?: () => void } = $props();

  let name = $state("");
  let color = $state("#10b981");
  let loading = $state(false);
  let error = $state("");

  const colorPresets = [
    { name: "Green", value: "#10b981" },
    { name: "Blue", value: "#3b82f6" },
    { name: "Purple", value: "#8b5cf6" },
    { name: "Red", value: "#ef4444" },
    { name: "Orange", value: "#f59e0b" },
    { name: "Pink", value: "#ec4899" },
    { name: "Cyan", value: "#06b6d4" },
    { name: "Yellow", value: "#eab308" },
  ];

  async function handleSubmit() {
    error = "";
    
    if (!name.trim()) {
      error = "Category name is required";
      return;
    }

    loading = true;
    try {
      await categoriesApi.create(name.trim(), color);
      open = false;
      name = "";
      color = "#10b981";
      onSuccess?.();
    } catch (err: any) {
      error = err.message || "Failed to create category";
    } finally {
      loading = false;
    }
  }

  function handleOpenChange(isOpen: boolean) {
    open = isOpen;
    if (!isOpen) {
      name = "";
      color = "#10b981";
      error = "";
    }
  }
</script>

<Dialog.Root bind:open onOpenChange={handleOpenChange}>
  <Dialog.Content class="sm:max-w-[425px]">
    <Dialog.Header>
      <Dialog.Title>Add Category</Dialog.Title>
      <Dialog.Description>
        Create a new category to organize your expenses
      </Dialog.Description>
    </Dialog.Header>

    <div class="grid gap-4 py-4">
      <div class="space-y-2">
        <Label for="name">Category Name</Label>
        <Input
          id="name"
          placeholder="e.g., Groceries, Transportation"
          bind:value={name}
          disabled={loading}
        />
      </div>

      <div class="space-y-2">
        <Label>Color</Label>
        <div class="grid grid-cols-4 gap-2">
          {#each colorPresets as preset}
            <button
              type="button"
              class="h-10 rounded-md border-2 transition-all hover:scale-110"
              class:ring-2={color === preset.value}
              class:ring-offset-2={color === preset.value}
              style="background-color: {preset.value}; border-color: {color === preset.value ? preset.value : 'transparent'}"
              onclick={() => color = preset.value}
              disabled={loading}
              title={preset.name}
            >
              {#if color === preset.value}
                <span class="text-white text-xl">✓</span>
              {/if}
            </button>
          {/each}
        </div>
        <div class="flex items-center gap-2 mt-2">
          <Input
            type="color"
            bind:value={color}
            disabled={loading}
            class="h-10 w-20 cursor-pointer"
          />
          <span class="text-sm text-muted-foreground">Or pick custom color</span>
        </div>
      </div>

      {#if error}
        <div class="text-sm text-destructive">{error}</div>
      {/if}
    </div>

    <Dialog.Footer>
      <Button variant="outline" onclick={() => open = false} disabled={loading}>
        Cancel
      </Button>
      <Button onclick={handleSubmit} disabled={loading}>
        {loading ? "Creating..." : "Create Category"}
      </Button>
    </Dialog.Footer>
  </Dialog.Content>
</Dialog.Root>
