<script setup lang="ts">
import { ref, computed } from 'vue';
import { TrendingUp, BarChart3, Wallet } from 'lucide-vue-next';

interface ChartData {
  date: string;
  income: number;
  expenses: number;
  balance: number;
}

const props = defineProps<{
  data: ChartData[];
  currency: string;
}>();

const hoverIndexA = ref<number | null>(null);
const hoverIndexB = ref<number | null>(null);

// Chart Dimensions (for each side-by-side panel)
const width = 500;
const height = 240;
const paddingLeft = 60;
const paddingRight = 15;
const paddingTop = 30;
const paddingBottom = 40;

const graphWidth = width - paddingLeft - paddingRight;
const graphHeight = height - paddingTop - paddingBottom;

// Formatting utilities
function formatRupiah(value: number) {
  if (value >= 1000000) {
    return `Rp ${(value / 1000000).toFixed(1)}jt`;
  }
  if (value >= 1000) {
    return `Rp ${(value / 1000).toFixed(0)}rb`;
  }
  return `Rp ${value}`;
}

function formatFullRupiah(value: number) {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(value);
}

// Extrema calculations for Chart A (Balance)
const maxBalance = computed(() => {
  if (props.data.length === 0) return 100000;
  const balances = props.data.map(d => d.balance);
  return Math.max(...balances) * 1.15;
});

const minBalance = computed(() => {
  if (props.data.length === 0) return 0;
  const balances = props.data.map(d => d.balance);
  return Math.max(0, Math.min(...balances) * 0.85);
});

// Extrema calculations for Chart B (Transactions)
const maxTransaction = computed(() => {
  if (props.data.length === 0) return 10000;
  const amounts = props.data.flatMap(d => [d.income, d.expenses]);
  return Math.max(...amounts, 10000) * 1.15;
});

// Map values to coordinates
const getBalanceY = (val: number) => {
  const range = maxBalance.value - minBalance.value;
  if (range === 0) return paddingTop + graphHeight / 2;
  const pct = (val - minBalance.value) / range;
  return height - paddingBottom - (pct * graphHeight);
};

const getTxnY = (val: number) => {
  if (maxTransaction.value === 0) return height - paddingBottom;
  const pct = val / maxTransaction.value;
  return height - paddingBottom - (pct * graphHeight);
};

// Points calculation
const points = computed(() => {
  if (props.data.length === 0) return [];
  const step = graphWidth / Math.max(1, props.data.length - 1);
  return props.data.map((d, index) => {
    const x = paddingLeft + (index * step);
    return {
      ...d,
      x,
      yBalance: getBalanceY(d.balance),
      yIncome: getTxnY(d.income),
      yExpense: getTxnY(d.expenses),
      formattedDate: new Date(d.date).toLocaleDateString('id-ID', { day: 'numeric', month: 'short' })
    };
  });
});

// Chart A Line & Area Paths
const linePath = computed(() => {
  if (points.value.length === 0) return '';
  return points.value.map((p, idx) => {
    const command = idx === 0 ? 'M' : 'L';
    return `${command} ${p.x.toFixed(1)} ${p.yBalance.toFixed(1)}`;
  }).join(' ');
});

const areaPath = computed(() => {
  if (points.value.length === 0) return '';
  const first = points.value[0];
  const last = points.value[points.value.length - 1];
  const baselineY = height - paddingBottom;
  let path = linePath.value;
  path += ` L ${last.x.toFixed(1)} ${baselineY}`;
  path += ` L ${first.x.toFixed(1)} ${baselineY} Z`;
  return path;
});

// Y-Axis Ticks (A and B)
const yTicksA = computed(() => {
  const ticks = 4;
  const list = [];
  const range = maxBalance.value - minBalance.value;
  for (let i = 0; i <= ticks; i++) {
    const val = minBalance.value + (range * (i / ticks));
    list.push({
      value: val,
      y: getBalanceY(val),
      label: formatRupiah(val)
    });
  }
  return list;
});

const yTicksB = computed(() => {
  const ticks = 4;
  const list = [];
  const range = maxTransaction.value;
  for (let i = 0; i <= ticks; i++) {
    const val = (range * (i / ticks));
    list.push({
      value: val,
      y: getTxnY(val),
      label: formatRupiah(val)
    });
  }
  return list;
});
</script>

<template>
  <div class="space-y-6">
    <!-- No-Data placeholder inside charts -->
    <div v-if="data.length === 0" class="bg-white rounded-3xl border border-slate-200/70 p-12 shadow-sm text-center select-none">
      <div class="w-14 h-14 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-center text-slate-400 mx-auto mb-4">
        <Wallet class="w-6 h-6 text-slate-450 animate-pulse" />
      </div>
      <h4 class="text-md font-black text-slate-800">Menunggu Unggahan Laporan</h4>
      <p class="text-xs text-slate-500 font-semibold max-w-sm mx-auto leading-relaxed mt-1">
        Grafik visualisasi saldo kas dan arus transaksi otomatis terbuat setelah rekening koran diunggah.
      </p>
    </div>

    <!-- Dual side-by-side layout charts -->
    <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      
      <!-- CHART A: Tren Saldo Kas -->
      <div class="bg-white rounded-3xl border border-slate-200/70 p-5 md:p-6 shadow-md relative flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between mb-3 select-none">
            <h4 class="text-sm font-black text-slate-800 flex items-center gap-2">
              <TrendingUp class="w-4.5 h-4.5 text-emerald-600" />
              Chart A: Tren Saldo Kas
            </h4>
            <span class="text-[9px] font-black uppercase tracking-wider text-emerald-600 bg-emerald-50 border border-emerald-100 px-2 py-0.5 rounded-md">
              Tren Saldo
            </span>
          </div>
          <p class="text-[11px] text-slate-500 font-semibold mb-4 select-none">Evolusi dan progresi harian saldo penutupan rekening koran</p>
        </div>

        <div class="relative w-full overflow-x-auto">
          <svg :viewBox="`0 0 ${width} ${height}`" class="w-full h-auto min-w-[360px]">
            <defs>
              <linearGradient id="balanceGlowA" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#10b981" stop-opacity="0.22" />
                <stop offset="100%" stop-color="#10b981" stop-opacity="0.0" />
              </linearGradient>
            </defs>

            <!-- Horizontal Grid lines -->
            <g stroke="#f1f5f9" stroke-width="0.75">
              <line 
                v-for="tick in yTicksA" 
                :key="'grid-a-'+tick.value" 
                :x1="paddingLeft" 
                :y1="tick.y" 
                :x2="width - paddingRight" 
                :y2="tick.y" 
              />
            </g>

            <!-- Y Axis Labels -->
            <g fill="#94a3b8" font-size="9" font-family="monospace" text-anchor="end" font-weight="bold">
              <text 
                v-for="tick in yTicksA" 
                :key="'label-a-'+tick.value" 
                :x="paddingLeft - 8" 
                :y="tick.y + 3"
              >
                {{ tick.label }}
              </text>
            </g>

            <!-- Gradient Area Fill -->
            <path :d="areaPath" fill="url(#balanceGlowA)" />

            <!-- Core Line Curve -->
            <path 
              :d="linePath" 
              fill="none" 
              stroke="#10b981" 
              stroke-width="2.2" 
              stroke-linecap="round"
              stroke-linejoin="round"
            />

            <!-- Scanline Tracker on Hover -->
            <line 
              v-if="hoverIndexA !== null && points[hoverIndexA]"
              :x1="points[hoverIndexA].x" 
              :y1="paddingTop" 
              :x2="points[hoverIndexA].x" 
              :y2="height - paddingBottom" 
              stroke="#cbd5e1" 
              stroke-width="1.2" 
              stroke-dasharray="3 3"
            />

            <!-- Interactive Hover Area Trigger Dots -->
            <g>
              <g 
                v-for="(p, idx) in points" 
                :key="'pt-a-'+idx"
                @mouseenter="hoverIndexA = idx"
                @mouseleave="hoverIndexA = null"
                class="cursor-pointer"
              >
                <circle 
                  v-if="hoverIndexA === idx"
                  :cx="p.x" 
                  :cy="p.yBalance" 
                  r="6" 
                  fill="#10b981" 
                  opacity="0.25"
                />
                <circle 
                  :cx="p.x" 
                  :cy="p.yBalance" 
                  :r="hoverIndexA === idx ? 4 : 2.5" 
                  :fill="hoverIndexA === idx ? '#ffffff' : '#10b981'" 
                  stroke="#10b981" 
                  :stroke-width="hoverIndexA === idx ? 2 : 1"
                />
                <rect 
                  :x="p.x - 10" 
                  :y="paddingTop" 
                  width="20" 
                  :height="graphHeight" 
                  fill="transparent"
                />
              </g>
            </g>

            <!-- X Axis Dates Timeline -->
            <g fill="#94a3b8" font-size="8.5" font-family="monospace" text-anchor="middle" font-weight="bold">
              <text 
                v-for="(p, idx) in points" 
                :key="'x-a-'+idx"
                v-show="points.length <= 8 || idx % Math.ceil(points.length / 6) === 0 || idx === points.length - 1"
                :x="p.x" 
                :y="height - paddingBottom + 16"
              >
                {{ p.formattedDate }}
              </text>
            </g>

            <!-- Baseline border -->
            <line 
              :x1="paddingLeft" 
              :y1="height - paddingBottom" 
              :x2="width - paddingRight" 
              :y2="height - paddingBottom" 
              stroke="#cbd5e1" 
              stroke-width="1" 
            />
          </svg>

          <!-- Chart A Hover Floating Tooltip details -->
          <div 
            v-if="hoverIndexA !== null && points[hoverIndexA]"
            class="absolute z-20 bg-slate-900/95 backdrop-blur-sm text-white px-3 py-2 rounded-xl border border-slate-800 shadow-lg pointer-events-none flex flex-col gap-0.5 w-44 text-[11px]"
            :style="{
              left: `${(points[hoverIndexA].x / width) * 100}%`,
              top: `15%`,
              transform: `translateX(-50%)`
            }"
          >
            <div class="font-black text-slate-400 border-b border-slate-800 pb-1 mb-1 font-mono uppercase text-[9px]">
              Tanggal: {{ points[hoverIndexA].formattedDate }}
            </div>
            <div class="flex items-center justify-between font-semibold">
              <span class="text-slate-300">Saldo Kas:</span>
              <span class="font-bold text-emerald-400 font-mono">{{ formatFullRupiah(points[hoverIndexA].balance) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- CHART B: Transaksi Masuk vs Keluar -->
      <div class="bg-white rounded-3xl border border-slate-200/70 p-5 md:p-6 shadow-md relative flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between mb-3 select-none">
            <h4 class="text-sm font-black text-slate-800 flex items-center gap-2">
              <BarChart3 class="w-4.5 h-4.5 text-indigo-600" />
              Chart B: Transaksi Masuk vs Keluar
            </h4>
            <span class="text-[9px] font-black uppercase tracking-wider text-indigo-600 bg-indigo-50 border border-indigo-100 px-2 py-0.5 rounded-md">
              Arus Kas
            </span>
          </div>
          <p class="text-[11px] text-slate-500 font-semibold mb-4 select-none">Komparasi volume transaksi harian masuk (inflow) vs keluar (outflow)</p>
        </div>

        <div class="relative w-full overflow-x-auto">
          <svg :viewBox="`0 0 ${width} ${height}`" class="w-full h-auto min-w-[360px]">
            <!-- Horizontal Grid lines -->
            <g stroke="#f1f5f9" stroke-width="0.75">
              <line 
                v-for="tick in yTicksB" 
                :key="'grid-b-'+tick.value" 
                :x1="paddingLeft" 
                :y1="tick.y" 
                :x2="width - paddingRight" 
                :y2="tick.y" 
              />
            </g>

            <!-- Y Axis Labels -->
            <g fill="#94a3b8" font-size="9" font-family="monospace" text-anchor="end" font-weight="bold">
              <text 
                v-for="tick in yTicksB" 
                :key="'label-b-'+tick.value" 
                :x="paddingLeft - 8" 
                :y="tick.y + 3"
              >
                {{ tick.label }}
              </text>
            </g>

            <!-- Side-by-Side Inflow & Outflow Bars -->
            <g opacity="0.95">
              <g v-for="(p, idx) in points" :key="'bars-b-'+idx" class="group/bar">
                <!-- Income Inflow Bar (Emerald) -->
                <rect 
                  v-if="p.income > 0"
                  :x="p.x - 4"
                  :y="p.yIncome"
                  width="3.5"
                  :height="Math.max(1, height - paddingBottom - p.yIncome)"
                  rx="1"
                  fill="#10b981"
                  opacity="0.85"
                />

                <!-- Expenses Outflow Bar (Rose) -->
                <rect 
                  v-if="p.expenses > 0"
                  :x="p.x + 0.5"
                  :y="p.yExpense"
                  width="3.5"
                  :height="Math.max(1, height - paddingBottom - p.yExpense)"
                  rx="1"
                  fill="#f43f5e"
                  opacity="0.85"
                />
              </g>
            </g>

            <!-- Scanline Tracker on Hover -->
            <line 
              v-if="hoverIndexB !== null && points[hoverIndexB]"
              :x1="points[hoverIndexB].x" 
              :y1="paddingTop" 
              :x2="points[hoverIndexB].x" 
              :y2="height - paddingBottom" 
              stroke="#cbd5e1" 
              stroke-width="1.2" 
              stroke-dasharray="3 3"
            />

            <!-- Interactive Hover Area Triggers -->
            <g>
              <g 
                v-for="(p, idx) in points" 
                :key="'pt-b-'+idx"
                @mouseenter="hoverIndexB = idx"
                @mouseleave="hoverIndexB = null"
                class="cursor-pointer"
              >
                <rect 
                  :x="p.x - 8" 
                  :y="paddingTop" 
                  width="16" 
                  :height="graphHeight" 
                  fill="transparent"
                />
              </g>
            </g>

            <!-- X Axis Dates Timeline -->
            <g fill="#94a3b8" font-size="8.5" font-family="monospace" text-anchor="middle" font-weight="bold">
              <text 
                v-for="(p, idx) in points" 
                :key="'x-b-'+idx"
                v-show="points.length <= 8 || idx % Math.ceil(points.length / 6) === 0 || idx === points.length - 1"
                :x="p.x" 
                :y="height - paddingBottom + 16"
              >
                {{ p.formattedDate }}
              </text>
            </g>

            <!-- Baseline border -->
            <line 
              :x1="paddingLeft" 
              :y1="height - paddingBottom" 
              :x2="width - paddingRight" 
              :y2="height - paddingBottom" 
              stroke="#cbd5e1" 
              stroke-width="1" 
            />
          </svg>

          <!-- Chart B Hover Floating Tooltip details -->
          <div 
            v-if="hoverIndexB !== null && points[hoverIndexB]"
            class="absolute z-20 bg-slate-900/95 backdrop-blur-sm text-white px-3 py-2.5 rounded-xl border border-slate-800 shadow-lg pointer-events-none flex flex-col gap-1 w-44 text-[11px]"
            :style="{
              left: `${(points[hoverIndexB].x / width) * 100}%`,
              top: `15%`,
              transform: `translateX(-50%)`
            }"
          >
            <div class="font-black text-slate-400 border-b border-slate-800 pb-1 mb-1 font-mono uppercase text-[9px]">
              Tanggal: {{ points[hoverIndexB].formattedDate }}
            </div>
            <div class="flex items-center justify-between">
              <span class="text-slate-300">Inflow (+):</span>
              <span class="font-bold text-emerald-400 font-mono">{{ formatRupiah(points[hoverIndexB].income) }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-slate-300">Outflow (-):</span>
              <span class="font-bold text-rose-400 font-mono">{{ formatRupiah(points[hoverIndexB].expenses) }}</span>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>
