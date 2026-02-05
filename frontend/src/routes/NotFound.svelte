<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import * as Card from "$lib/components/ui/card";
  import { Home, ArrowLeft } from "lucide-svelte";
</script>

<div class="flex min-h-screen items-center justify-center bg-muted/50 p-4">
  <Card.Root class="w-full max-w-md text-center">
    <Card.Content class="pt-12 pb-8">
      <div class="mb-6 inline-flex h-20 w-20 items-center justify-center rounded-full bg-muted">
        <span class="text-4xl">🔍</span>
      </div>
      
      <h1 class="text-6xl font-bold mb-2">404</h1>
      <h2 class="text-2xl font-semibold mb-3">Page Not Found</h2>
      <p class="text-muted-foreground mb-8">
        Sorry, the page you're looking for doesn't exist or has been moved.
      </p>

      <div class="flex flex-col sm:flex-row gap-3 justify-center">
        <Button size="lg" class="gap-2" onclick={() => window.history.back()}>
          <ArrowLeft size={18} />
          Go Back
        </Button>
        <Button variant="outline" size="lg" class="gap-2" onclick={() => window.location.hash = "#/dashboard"}>
          <Home size={18} />
          Go Home
        </Button>
      </div>
    </Card.Content>
  </Card.Root>
</div>
