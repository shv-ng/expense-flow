<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import type { ChartConfiguration } from 'chart.js';

  let {
    data,
    options = {},
  }: {
    data: { labels: string[]; datasets: any[] };
    options?: any;
  } = $props();

  let canvas: HTMLCanvasElement;
  let chart: any;

  async function createChart() {
    // Dynamically import Chart.js to avoid SSR issues
    const { Chart, registerables } = await import('chart.js');
    Chart.register(...registerables);

    if (chart) {
      chart.destroy();
    }

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const config: ChartConfiguration = {
      type: 'doughnut',
      data: $state.snapshot(data),
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              padding: 15,
              font: {
                size: 12,
              },
            },
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                const label = context.label || '';
                const value = context.parsed;
                const total = context.dataset.data.reduce((a: number, b: number) => a + b, 0);
                const percentage = ((value / total) * 100).toFixed(1);
                return `${label}: $${value.toFixed(2)} (${percentage}%)`;
              }
            }
          },
        },
        ...options,
      },
    };

    chart = new Chart(ctx, config);
  }

  onMount(() => {
    createChart();
  });

  $effect(() => {
    if (chart && data) {
      chart.data = $state.snapshot(data);
      chart.update();
    }
  });

  onDestroy(() => {
    if (chart) {
      chart.destroy();
    }
  });
</script>

<div class="relative w-full h-full">
  <canvas bind:this={canvas}></canvas>
</div>
