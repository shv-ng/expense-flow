<script lang="ts">
  import DashboardLayout from "$lib/components/DashboardLayout.svelte";
  import * as Card from "$lib/components/ui/card";
  import { Button } from "$lib/components/ui/button";
  import { TrendingUp, Calendar, DollarSign, PieChart } from "lucide-svelte";
  import LineChart from "$lib/components/LineChart.svelte";
  import PieChartComponent from "$lib/components/PieChart.svelte";
  import { onMount } from "svelte";
  import { analyticsApi } from "$lib/api/analytics";

  let loading = $state(true);
  let spendingByDate = $state<any>(null);
  let spendingByCategory = $state<any>(null);
  let spendingByMonth = $state<any>(null);

  const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  onMount(async () => {
    await loadAnalytics();
  });

  async function loadAnalytics() {
    loading = true;
    try {
      const [byDate, byCategory, byMonth] = await Promise.all([
        analyticsApi.getSpendingByDate(),
        analyticsApi.getSpendingByCategory(),
        analyticsApi.getSpendingByMonth(),
      ]);

      // Prepare data for Line Chart (Spending by Date)
      spendingByDate = {
        labels: byDate.labels,
        datasets: [
          {
            label: 'Daily Spending',
            data: byDate.data,
            borderColor: 'rgb(59, 130, 246)',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            tension: 0.4,
            fill: true,
          },
        ],
      };

      // Prepare data for Pie Chart (Spending by Category)
      const categoryColors = [
        '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', 
        '#ec4899', '#06b6d4', '#eab308', '#f97316', '#14b8a6'
      ];
      
      spendingByCategory = {
        labels: byCategory.labels,
        datasets: [
          {
            data: byCategory.data,
            backgroundColor: categoryColors.slice(0, byCategory.labels.length),
            borderWidth: 2,
            borderColor: '#fff',
          },
        ],
      };

      // Prepare data for Monthly Chart
      spendingByMonth = {
        labels: byMonth.labels.map(m => monthNames[m - 1]),
        datasets: [
          {
            label: 'Monthly Spending',
            data: byMonth.data,
            borderColor: 'rgb(168, 85, 247)',
            backgroundColor: 'rgba(168, 85, 247, 0.1)',
            tension: 0.4,
            fill: true,
          },
        ],
      };
    } catch (err) {
      console.error("Failed to load analytics:", err);
    } finally {
      loading = false;
    }
  }

  // Calculate totals
  let totalSpent = $derived(
    spendingByDate?.datasets[0]?.data?.reduce((a: number, b: number) => a + b, 0) || 0
  );
  let categoryCount = $derived(spendingByCategory?.labels?.length || 0);
  let averageDaily = $derived(
    spendingByDate?.datasets[0]?.data?.length > 0
      ? totalSpent / spendingByDate.datasets[0].data.length
      : 0
  );
</script>

<DashboardLayout>
  <div class="space-y-8">
    <!-- Header -->
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h2 class="text-3xl font-bold tracking-tight">Analytics</h2>
        <p class="text-muted-foreground mt-1">Visualize your spending patterns and trends</p>
      </div>
    </div>

    {#if loading}
      <div class="flex items-center justify-center py-12">
        <p class="text-muted-foreground">Loading analytics...</p>
      </div>
    {:else if !spendingByDate || spendingByDate.datasets[0].data.length === 0}
      <!-- Empty State -->
      <Card.Root>
        <Card.Content class="pt-12 pb-12">
          <div class="flex flex-col items-center justify-center text-center">
            <div class="rounded-full bg-muted p-6 mb-4">
              <TrendingUp size={48} class="text-muted-foreground" />
            </div>
            <h3 class="text-xl font-semibold mb-2">No data to analyze yet</h3>
            <p class="text-muted-foreground mb-6 max-w-sm">
              Start adding expenses to see your spending patterns and insights
            </p>
            <Button size="lg" onclick={() => window.location.hash = "#/expenses"}>
              Add Your First Expense
            </Button>
          </div>
        </Card.Content>
      </Card.Root>
    {:else}
      <!-- Summary Stats -->
      <div class="grid gap-4 sm:grid-cols-3">
        <Card.Root>
          <Card.Content class="pt-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-muted-foreground">Total Spending</p>
                <p class="text-2xl font-bold mt-1">${totalSpent.toFixed(2)}</p>
              </div>
              <div class="rounded-lg bg-blue-500/10 p-3">
                <DollarSign class="text-blue-600" size={22} />
              </div>
            </div>
          </Card.Content>
        </Card.Root>

        <Card.Root>
          <Card.Content class="pt-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-muted-foreground">Categories</p>
                <p class="text-2xl font-bold mt-1">{categoryCount}</p>
              </div>
              <div class="rounded-lg bg-purple-500/10 p-3">
                <PieChart class="text-purple-600" size={22} />
              </div>
            </div>
          </Card.Content>
        </Card.Root>

        <Card.Root>
          <Card.Content class="pt-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-muted-foreground">Daily Average</p>
                <p class="text-2xl font-bold mt-1">${averageDaily.toFixed(2)}</p>
              </div>
              <div class="rounded-lg bg-emerald-500/10 p-3">
                <Calendar class="text-emerald-600" size={22} />
              </div>
            </div>
          </Card.Content>
        </Card.Root>
      </div>

      <!-- Charts Grid -->
      <div class="grid gap-6 lg:grid-cols-2">
        <!-- Daily Spending Chart -->
        <Card.Root>
          <Card.Header>
            <Card.Title>Daily Spending Trend</Card.Title>
            <Card.Description>Your expenses over time</Card.Description>
          </Card.Header>
          <Card.Content>
            <div class="h-[300px]">
              {#if spendingByDate}
                <LineChart data={spendingByDate} />
              {/if}
            </div>
          </Card.Content>
        </Card.Root>

        <!-- Category Distribution Chart -->
        <Card.Root>
          <Card.Header>
            <Card.Title>Spending by Category</Card.Title>
            <Card.Description>Distribution across categories</Card.Description>
          </Card.Header>
          <Card.Content>
            <div class="h-[300px]">
              {#if spendingByCategory}
                <PieChartComponent data={spendingByCategory} />
              {/if}
            </div>
          </Card.Content>
        </Card.Root>
      </div>

      <!-- Monthly Trend Chart -->
      <Card.Root>
        <Card.Header>
          <Card.Title>Monthly Spending</Card.Title>
          <Card.Description>Compare your spending across months</Card.Description>
        </Card.Header>
        <Card.Content>
          <div class="h-[350px]">
            {#if spendingByMonth}
              <LineChart data={spendingByMonth} />
            {/if}
          </div>
        </Card.Content>
      </Card.Root>

      <!-- Category Breakdown Table -->
      {#if spendingByCategory && spendingByCategory.labels.length > 0}
        <Card.Root>
          <Card.Header>
            <Card.Title>Category Breakdown</Card.Title>
            <Card.Description>Detailed spending by category</Card.Description>
          </Card.Header>
          <Card.Content>
            <div class="space-y-4">
              {#each spendingByCategory.labels as label, index}
                {@const amount = spendingByCategory.datasets[0].data[index]}
                {@const percentage = (amount / totalSpent) * 100}
                {@const color = spendingByCategory.datasets[0].backgroundColor[index]}
                
                <div class="space-y-2">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center gap-2">
                      <div class="h-3 w-3 rounded-full" style="background-color: {color}"></div>
                      <span class="font-medium">{label}</span>
                    </div>
                    <div class="text-right">
                      <span class="font-bold">${amount.toFixed(2)}</span>
                      <span class="text-sm text-muted-foreground ml-2">({percentage.toFixed(1)}%)</span>
                    </div>
                  </div>
                  <div class="h-2 bg-muted rounded-full overflow-hidden">
                    <div 
                      class="h-full rounded-full transition-all" 
                      style="width: {percentage}%; background-color: {color}"
                    ></div>
                  </div>
                </div>
              {/each}
            </div>
          </Card.Content>
        </Card.Root>
      {/if}
    {/if}
  </div>
</DashboardLayout>
