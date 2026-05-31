<script setup lang="ts">
import { computed } from 'vue';
import { useFinancialStore, FinancialHealth } from '../../stores/financial';
import { useBusinessStore } from '../../stores/business';
import FinancialChart from './FinancialChart.vue';
import { 
  TrendingUp, TrendingDown, Wallet, CheckCircle2, 
  Lightbulb, ShieldAlert, ArrowRightLeft, Landmark,
  Building
} from 'lucide-vue-next';

const financialStore = useFinancialStore();
const businessStore = useBusinessStore();

// Format monetary values
function formatCurrency(val: number) {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(val);
}

// Map health status to nice descriptive labels and badge colors
const healthMeta = computed(() => {
  if (!financialStore.analysis) return { label: 'Tidak Diketahui', color: 'bg-slate-100 text-slate-800 border-slate-350', border: 'border-slate-350' };
  
  switch (financialStore.analysis.health_status) {
    case FinancialHealth.VERY_HEALTHY:
      return { 
        label: 'Sangat Sehat', 
        color: 'bg-emerald-50/80 text-emerald-900 border-emerald-300/70', 
        gaugeColor: '#10b981',
        desc: 'Bisnis memiliki fondasi likuiditas prima dan margin kontribusi sangat kuat.'
      };
    case FinancialHealth.HEALTHY:
      return { 
        label: 'Sehat', 
        color: 'bg-green-50/80 text-green-900 border-green-300/70', 
        gaugeColor: '#22c55e',
        desc: 'Arus kas stabil dengan perputaran piutang yang lancar.'
      };
    case FinancialHealth.MODERATE:
      return { 
        label: 'Cukup Sehat', 
        color: 'bg-amber-50/80 text-amber-900 border-amber-300/70', 
        gaugeColor: '#f59e0b',
        desc: 'Kondisi kas cukup, namun perlu waspada pada tren peningkatan biaya tetap (OPEX).'
      };
    case FinancialHealth.AT_RISK:
      return { 
        label: 'Beresiko', 
        color: 'bg-orange-50/80 text-orange-900 border-orange-300/70', 
        gaugeColor: '#f97316',
        desc: 'Arus kas ketat. Beban operasional menyerap sebagian besar surplus pemasukan.'
      };
    case FinancialHealth.DISTRESSED:
      return { 
        label: 'Kritis', 
        color: 'bg-rose-50/80 text-rose-900 border-rose-300/70', 
        gaugeColor: '#ef4444',
        desc: 'Kas defisit. Segera lakukan restrukturisasi biaya pokok (COGS) dan opex mendesak.'
      };
    default:
      return { label: 'Tidak Terdefinisi', color: 'bg-slate-50 text-slate-600', gaugeColor: '#94a3b8', desc: '' };
  }
});

// Calculations for the SVG semi-circle Gauge Chart
const gaugeDashoffset = computed(() => {
  if (!financialStore.analysis) return 220; // Empty gauge
  
  const score = financialStore.analysis.health_score;
  const radius = 70;
  const circumference = Math.PI * radius; // 219.9
  
  // Map score (0-100) to gauge fill (from 0 to circumference)
  // Dashoffset starts at circumference (empty) and goes to 0 (full)
  const percent = Math.min(100, Math.max(0, score)) / 100;
  return circumference * (1 - percent);
});
</script>

<template>
  <div class="space-y-8 font-sans">
    
    <!-- State A: No Business Registered Warning -->
    <div v-if="!businessStore.activeBusiness" class="max-w-2xl mx-auto bg-white rounded-3xl border border-rose-100 p-10 text-center shadow-lg relative overflow-hidden select-none">
      <div class="absolute -top-12 -left-12 w-48 h-48 bg-rose-500/5 blur-3xl rounded-full pointer-events-none"></div>
      <div class="space-y-6 max-w-md mx-auto">
        <div class="w-16 h-16 rounded-2xl bg-rose-50 border border-rose-100 text-rose-500 flex items-center justify-center mx-auto shadow-sm">
          <Building class="w-8 h-8" />
        </div>
        <h2 class="text-2xl font-black text-slate-800">Profil Bisnis Belum Terdaftar</h2>
        <p class="text-sm text-slate-500 font-semibold leading-relaxed">
          Sebelum memulai analisis keuangan, silakan daftarkan profil bisnis utama Anda terlebih dahulu di tab <span class="text-emerald-600 font-bold">Bisnis</span> agar data rekening koran dapat disinkronkan dengan benar.
        </p>
      </div>
    </div>

    <!-- State B: No Statements Uploaded Warning -->
    <div v-else-if="financialStore.reports.length === 0" class="max-w-2xl mx-auto bg-white rounded-3xl border border-amber-100 p-10 text-center shadow-lg relative overflow-hidden select-none">
      <div class="absolute -top-12 -left-12 w-48 h-48 bg-amber-500/5 blur-3xl rounded-full pointer-events-none"></div>
      <div class="space-y-6 max-w-md mx-auto">
        <div class="w-16 h-16 rounded-2xl bg-amber-50 border border-amber-100 text-amber-500 flex items-center justify-center mx-auto shadow-sm">
          <Landmark class="w-8 h-8" />
        </div>
        <h2 class="text-2xl font-black text-slate-800">Belum Ada Rekening Koran Diunggah</h2>
        <p class="text-sm text-slate-500 font-semibold leading-relaxed">
          Kesehatan likuiditas dan rasio profitabilitas bisnis Anda belum dapat dianalisis. Silakan buka tab <span class="text-emerald-600 font-bold">Bisnis</span> sub-tab <span class="text-emerald-600 font-bold">Keuangan &amp; Rekening Koran</span> dan unggah berkas rekening koran PDF Anda.
        </p>
      </div>
    </div>

    <!-- Active State: Financial Reports Dashboard -->
    <div v-else class="space-y-8 pb-16">
      
      <!-- Financial Overview Cards Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 font-sans items-stretch">
        <!-- Kas Akhir Card -->
        <div class="bg-white rounded-3xl border border-slate-200/60 p-6 shadow-md relative overflow-hidden h-full flex flex-col justify-between">
          <div class="absolute right-3 top-3 w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
            <Wallet class="w-5 h-5" />
          </div>
          <div>
            <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Saldo Akhir Kas</span>
            <p class="text-xl font-black mt-2 font-mono text-emerald-600">
              {{ formatCurrency(financialStore.activeReport?.bank_statement.final_balance || 0) }}
            </p>
          </div>
          <div class="text-[10px] text-slate-500 font-bold mt-2.5 flex items-center gap-1 font-mono">
            No. Rek: {{ financialStore.activeReport?.bank_statement.account_number }}
          </div>
        </div>

        <!-- Total Masuk Card -->
        <div class="bg-white rounded-3xl border border-slate-200/60 p-6 shadow-md relative overflow-hidden h-full flex flex-col justify-between">
          <div class="absolute right-3 top-3 w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
            <TrendingUp class="w-5 h-5" />
          </div>
          <div>
            <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Total Pemasukan</span>
            <p class="text-xl font-black mt-2 font-mono text-emerald-600">
              {{ formatCurrency(financialStore.totalInflow) }}
            </p>
          </div>
          <div class="text-[10px] text-emerald-900 font-black mt-2.5 inline-flex items-center gap-0.5 bg-emerald-50/80 border border-emerald-200/60 px-2 py-1 rounded-md self-start">
            Arus Masuk (+)
          </div>
        </div>

        <!-- Total Keluar Card -->
        <div class="bg-white rounded-3xl border border-slate-200/60 p-6 shadow-md relative overflow-hidden h-full flex flex-col justify-between">
          <div class="absolute right-3 top-3 w-10 h-10 rounded-xl bg-rose-50 text-rose-500 flex items-center justify-center">
            <TrendingDown class="w-5 h-5" />
          </div>
          <div>
            <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Total Pengeluaran</span>
            <p class="text-xl font-black mt-2 font-mono text-rose-600">
              {{ formatCurrency(financialStore.totalOutflow) }}
            </p>
          </div>
          <div class="text-[10px] text-rose-900 font-black mt-2.5 inline-flex items-center gap-0.5 bg-rose-50/80 border border-rose-200/60 px-2 py-1 rounded-md self-start">
            Arus Keluar (-)
          </div>
        </div>

        <!-- Arus Kas Bersih Card -->
        <div class="bg-white rounded-3xl border border-slate-200/60 p-6 shadow-md relative overflow-hidden h-full flex flex-col justify-between">
          <div class="absolute right-3 top-3 w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
            <ArrowRightLeft class="w-5 h-5" />
          </div>
          <div>
            <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Arus Kas Bersih</span>
            <p :class="['text-xl font-black mt-2 font-mono', financialStore.netCashFlow >= 0 ? 'text-emerald-600' : 'text-rose-600']">
              {{ formatCurrency(financialStore.netCashFlow) }}
            </p>
          </div>
          <div class="text-[10px] font-bold mt-2.5 flex">
            <span v-if="financialStore.netCashFlow >= 0" class="text-emerald-900 font-black bg-emerald-50/80 px-2 py-1 rounded-md border border-emerald-200/60">Surplus Kas</span>
            <span v-else class="text-rose-900 font-black bg-rose-50/80 px-2 py-1 rounded-md border border-rose-200/60">Defisit Kas</span>
          </div>
        </div>
      </div>

      <!-- Financial Health Score Gauge & AI analysis columns -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        <!-- SVG Gauge Chart card (takes 4 cols) -->
        <div class="lg:col-span-4 bg-white rounded-3xl border border-slate-200/60 p-6 shadow-md flex flex-col items-center text-center animate-fade-in">
          <div class="self-start select-none">
            <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Metrik Kesehatan</span>
            <h3 class="text-base font-black text-slate-850 mt-2 block">Skor Kesehatan Keuangan</h3>
          </div>

          <!-- SVG Semi-Circular Gauge Component -->
          <div class="relative w-52 h-36 flex items-center justify-center mt-6 select-none">
            <svg viewBox="0 0 160 100" class="w-full h-full">
              <!-- Background semi-circle track -->
              <path 
                d="M 10 90 A 70 70 0 0 1 150 90" 
                fill="none" 
                stroke="#f1f5f9" 
                stroke-width="14" 
                stroke-linecap="round"
              />
              
              <!-- Active progress colored track -->
              <path 
                d="M 10 90 A 70 70 0 0 1 150 90" 
                fill="none" 
                :stroke="healthMeta.gaugeColor" 
                stroke-width="14" 
                stroke-linecap="round"
                stroke-dasharray="220" 
                :stroke-dashoffset="gaugeDashoffset"
                class="transition-all duration-1000 ease-out"
              />
            </svg>
            
            <!-- Floating values inside the gauge core (Centered within donut arc) -->
            <div class="absolute bottom-7 text-center flex flex-col gap-1">
              <span class="text-3xl font-black font-mono text-slate-850 tracking-tighter">
                {{ financialStore.analysis?.health_score.toFixed(1) }}
              </span>
              <span :class="['badge font-black uppercase text-[9px] tracking-wider px-2.5 py-1.5 border shadow-xs', healthMeta.color]">
                {{ healthMeta.label }}
              </span>
            </div>
          </div>

          <!-- Description HUD -->
          <div class="bg-slate-50 border border-slate-100/80 rounded-2xl p-4 w-full mt-4 font-sans select-none">
            <p class="text-xs text-slate-600 leading-relaxed font-semibold">
              {{ healthMeta.desc }}
            </p>
          </div>
        </div>

        <!-- AI insights, Warnings & Recommendations columns (takes 8 cols) - Refactored into a cohesive section of themed cards -->
        <div class="lg:col-span-8 space-y-6">
          <div class="space-y-4">
            <div class="select-none">
              <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Analisis Komprehensif</span>
              <h3 class="text-base font-black text-slate-850 mt-0.5">Laporan Rekomendasi Finansial Vantage AI</h3>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 font-sans">
              <!-- Insights Card (Emerald Theme) -->
              <div class="bg-emerald-50/20 border border-emerald-100 p-5 rounded-2xl shadow-xs flex flex-col justify-between">
                <div class="space-y-4">
                  <h4 class="text-xs font-black text-emerald-800 uppercase tracking-wider flex items-center gap-1.5 select-none">
                    <CheckCircle2 class="w-4.5 h-4.5 text-emerald-500 shrink-0" />
                    Sorotan Positif
                  </h4>
                  <ul class="text-[11px] text-slate-700 font-semibold space-y-3 leading-relaxed">
                    <li v-for="(ins, idx) in financialStore.analysis?.insights" :key="'ins-'+idx" class="flex gap-1.5 items-start">
                      <span class="w-1 h-1 rounded-full bg-emerald-500 shrink-0 mt-1.5"></span>
                      <span>{{ ins }}</span>
                    </li>
                  </ul>
                </div>
              </div>

              <!-- Warnings Card (Rose Theme) -->
              <div class="bg-rose-50/20 border border-rose-100 p-5 rounded-2xl shadow-xs flex flex-col justify-between">
                <div class="space-y-4">
                  <h4 class="text-xs font-black text-rose-800 uppercase tracking-wider flex items-center gap-1.5 select-none">
                    <ShieldAlert class="w-4.5 h-4.5 text-rose-500 shrink-0" />
                    Aspek Resiko
                  </h4>
                  <ul class="text-[11px] text-slate-700 font-semibold space-y-3 leading-relaxed">
                    <li v-for="(warn, idx) in financialStore.analysis?.warnings" :key="'warn-'+idx" class="flex gap-1.5 items-start">
                      <span class="w-1 h-1 rounded-full bg-rose-500 shrink-0 mt-1.5"></span>
                      <span>{{ warn }}</span>
                    </li>
                  </ul>
                </div>
              </div>

              <!-- Recommendations Card (Sky Theme) -->
              <div class="bg-sky-50/20 border border-sky-100 p-5 rounded-2xl shadow-xs flex flex-col justify-between">
                <div class="space-y-4">
                  <h4 class="text-xs font-black text-sky-800 uppercase tracking-wider flex items-center gap-1.5 select-none">
                    <Lightbulb class="w-4.5 h-4.5 text-sky-500 shrink-0" />
                    Rekomendasi Strategis
                  </h4>
                  <ul class="text-[11px] text-slate-700 font-semibold space-y-3 leading-relaxed">
                    <li v-for="(rec, idx) in financialStore.analysis?.recommendations" :key="'rec-'+idx" class="flex gap-1.5 items-start">
                      <span class="w-1 h-1 rounded-full bg-sky-500 shrink-0 mt-1.5"></span>
                      <span>{{ rec }}</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- Financial Charts & Cashflow trends visualizer (Dual high-fidelity charts render here) -->
      <div>
        <FinancialChart 
          :data="financialStore.dailyBalances"
          :currency="financialStore.activeReport?.bank_statement.currency || 'IDR'"
        />
      </div>

      <!-- Expense and Category Breakdown progress dashboard with Subcategory detail items -->
      <div class="bg-white rounded-3xl border border-slate-200/60 p-6 shadow-md">
        <div class="mb-6 select-none">
          <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Struktur Alokasi Kas</span>
          <h3 class="text-base font-black text-slate-800 mt-0.5">Analisis Pengeluaran &amp; Pemasukan per Kategori</h3>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 font-sans">
          <div 
            v-for="(amount, category) in financialStore.categoryTotals" 
            :key="category"
            class="bg-slate-50 border border-slate-100 p-4.5 rounded-2xl flex flex-col gap-2.5"
          >
            <div class="flex items-center justify-between text-xs font-bold text-slate-700">
              <span class="truncate max-w-[240px] text-slate-850">{{ category }}</span>
              <span class="font-mono font-black text-slate-900">{{ formatCurrency(amount) }}</span>
            </div>
            
            <!-- Color category progress bar dynamically -->
            <div class="w-full bg-slate-200/70 rounded-full h-2.5 overflow-hidden mb-1">
              <div 
                :class="[
                  'h-full rounded-full transition-all duration-500',
                  category.includes('Pendapatan') ? 'bg-emerald-500' : (category.includes('OPEX') || category.includes('COGS') ? 'bg-rose-500' : 'bg-slate-500')
                ]" 
                :style="{ width: Math.min(100, (amount / Math.max(1, financialStore.totalInflow)) * 100) + '%' }"
              ></div>
            </div>

            <!-- Expose & Render Subcategory Breakdown List Details -->
            <div 
              v-if="financialStore.subcategoryTotals[category]" 
              class="border-t border-slate-200/60 pt-2.5 space-y-1.5 mt-1"
            >
              <div 
                v-for="(subAmt, subcat) in financialStore.subcategoryTotals[category]" 
                :key="subcat"
                class="flex items-center justify-between text-[11px] text-slate-600 font-semibold pl-1"
              >
                <span class="truncate max-w-[180px] text-slate-500">{{ subcat }}</span>
                <span class="font-mono font-bold text-slate-700">{{ formatCurrency(subAmt) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>

  </div>
</template>
