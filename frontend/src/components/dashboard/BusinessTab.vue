<script setup lang="ts">
import { ref, computed } from 'vue';
import { useBusinessStore } from '../../stores/business';
import { useFinancialStore } from '../../stores/financial';
import CompetitorsTab from './CompetitorsTab.vue';
import StatementsTab from './StatementsTab.vue';
import { 
  Building, Sparkles, 
  AlertCircle, Landmark, Compass
} from 'lucide-vue-next';

const businessStore = useBusinessStore();
const financialStore = useFinancialStore();

// Sub-tab selection state: 'competitors' | 'statements'
const activeSubTab = ref<'competitors' | 'statements'>('competitors');

// Form states for new business with validation
const bizName = ref('');
const bizIndustry = ref('Food & Beverage');
const bizUrl = ref('');
const submitError = ref('');

const isBizNameTouched = ref(false);
const isBizUrlTouched = ref(false);

const isBizNameValid = computed(() => {
  return bizName.value.trim().length > 0;
});

const isBizUrlValid = computed(() => {
  const url = bizUrl.value.trim();
  if (!url) return false;
  return url.includes('maps.google.com') || url.includes('google.com/maps') || url.includes('maps.app.goo.gl');
});

async function handleCreateBusiness() {
  isBizNameTouched.value = true;
  isBizUrlTouched.value = true;
  submitError.value = '';
  
  if (!isBizNameValid.value || !isBizUrlValid.value) {
    submitError.value = 'Silakan perbaiki kesalahan pada formulir di bawah.';
    return;
  }

  try {
    await businessStore.createBusiness(bizName.value, bizIndustry.value, bizUrl.value);
    financialStore.loadDemoData();
  } catch (err: any) {
    submitError.value = err.message || 'Gagal menganalisis bisnis.';
  }
}
</script>

<template>
  <div class="space-y-8 font-sans">
    
    <!-- Onboarding State: Add Business Form (Single Business Limit) -->
    <div v-if="!businessStore.activeBusiness" class="max-w-xl mx-auto bg-white rounded-2xl border border-slate-200/80 p-8 md:p-10 shadow-lg relative overflow-hidden">
      <div class="absolute -top-12 -left-12 w-48 h-48 bg-emerald-500/5 blur-3xl rounded-full pointer-events-none"></div>
      
      <div class="text-center space-y-3 mb-8 relative z-10 select-none">
        <div class="w-14 h-14 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center mx-auto shadow-sm">
          <Building class="w-7 h-7" />
        </div>
        <h2 class="text-2xl font-black text-slate-800">Daftarkan Bisnis Anda</h2>
        <p class="text-xs text-slate-500 font-semibold leading-relaxed">
          Vantage AI mengunci akun Anda ke satu profil bisnis utama agar model pembelajaran rasio & SWOT geospasial bekerja terfokus.
        </p>
      </div>

      <form @submit.prevent="handleCreateBusiness" class="space-y-5 relative z-10 font-sans">
        <div class="form-control w-full">
          <label class="label"><span class="label-text font-black text-slate-700 text-[10px] uppercase tracking-wider">Nama Bisnis</span></label>
          <input 
            type="text" 
            v-model="bizName"
            @blur="isBizNameTouched = true"
            placeholder="Contoh: Kopi Nusantara Senopati" 
            :class="[
              'input input-bordered focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 rounded-xl text-xs font-semibold w-full text-slate-800',
              { 'border-rose-500 focus:border-rose-500 focus:ring-rose-500': isBizNameTouched && !isBizNameValid }
            ]" 
          />
          <p v-if="isBizNameTouched && !isBizNameValid" class="text-[10px] text-rose-500 font-bold mt-1">Nama bisnis tidak boleh kosong.</p>
        </div>

        <div class="form-control w-full">
          <label class="label"><span class="label-text font-black text-slate-700 text-[10px] uppercase tracking-wider">Kategori Industri</span></label>
          <select v-model="bizIndustry" class="select select-bordered focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 rounded-xl text-xs font-semibold w-full text-slate-850">
            <option>Food & Beverage</option>
            <option>Retail Jasa / Dagang</option>
            <option>Kecantikan & Salon</option>
            <option>Fashion & Pakaian</option>
          </select>
        </div>

        <div class="form-control w-full">
          <label class="label">
            <span class="label-text font-black text-slate-700 text-[10px] uppercase tracking-wider">Link Google Maps Bisnis</span>
          </label>
          <input 
            type="url" 
            v-model="bizUrl"
            @blur="isBizUrlTouched = true"
            placeholder="https://maps.google.com/?q=..." 
            :class="[
              'input input-bordered focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 rounded-xl text-xs font-semibold w-full text-slate-800',
              { 'border-rose-500 focus:border-rose-500 focus:ring-rose-500': isBizUrlTouched && !isBizUrlValid }
            ]" 
          />
          <p v-if="isBizUrlTouched && !isBizUrlValid" class="text-[10px] text-rose-500 font-bold mt-1">Masukkan URL Google Maps yang valid (mengandung maps.google.com, google.com/maps, atau maps.app.goo.gl).</p>
          <label class="label">
            <span class="label-text-alt text-[9px] font-bold text-slate-400">Salin link share lokasi dari penelusuran Google Maps Anda</span>
          </label>
        </div>

        <div v-if="submitError" class="alert alert-error rounded-xl py-2.5 px-3 text-xs font-bold flex gap-2">
          <AlertCircle class="w-4 h-4 shrink-0" />
          <span>{{ submitError }}</span>
        </div>

        <button 
          type="submit" 
          :disabled="businessStore.loading" 
          class="btn w-full bg-gradient-to-r from-emerald-500 to-teal-600 text-white rounded-xl font-bold border-none hover:from-emerald-600 hover:to-teal-700 shadow-md shadow-emerald-500/10 min-h-0 h-11"
        >
          <span v-if="businessStore.loading" class="loading loading-spinner loading-sm"></span>
          <span v-else class="flex items-center gap-1.5"><Sparkles class="w-4 h-4" /> Daftarkan Profil Bisnis</span>
        </button>
      </form>
    </div>

    <!-- Active State: Core Business Profile Information -->
    <div v-else class="w-full space-y-6">
      
      <!-- Premium B2B Brand Header -->
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 select-none pb-2 border-b border-slate-100">
        <div>
          <h1 class="text-2xl font-black text-slate-850 flex items-center gap-2.5">
            Vantage AI Growth Center
            <span class="badge bg-emerald-100 border border-emerald-200 text-emerald-800 text-[9.5px] font-black uppercase tracking-widest px-2 py-1 rounded-md animate-pulse">Live</span>
          </h1>
          <p class="text-xs text-slate-550 font-bold mt-1.5">Platform Pemetaan Geospasial, SWOT AI, &amp; Audit Finansial Bisnis Anda</p>
        </div>
      </div>

      <!-- Growth Suite Processing HUD -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 select-none font-sans">
        <div class="bg-white rounded-2xl border border-slate-250/60 p-4 shadow-xs flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center shrink-0">
            <Compass class="w-5 h-5" />
          </div>
          <div>
            <span class="text-[9px] font-black text-slate-550 uppercase tracking-widest block">Peta Geospasial</span>
            <span class="text-xs font-black text-slate-700 flex items-center gap-1.5 mt-0.5">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              Selesai Terpetakan
            </span>
          </div>
        </div>
        <div class="bg-white rounded-2xl border border-slate-250/60 p-4 shadow-xs flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center shrink-0">
            <Sparkles class="w-5 h-5" />
          </div>
          <div>
            <span class="text-[9px] font-black text-slate-550 uppercase tracking-widest block">Analisis AI SWOT</span>
            <span class="text-xs font-black text-slate-700 flex items-center gap-1.5 mt-0.5">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              Aktif &amp; Optimal
            </span>
          </div>
        </div>
        <div class="bg-white rounded-2xl border border-slate-250/60 p-4 shadow-xs flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center shrink-0">
            <Landmark class="w-5 h-5" />
          </div>
          <div>
            <span class="text-[9px] font-black text-slate-550 uppercase tracking-widest block">Audit Rekening Koran</span>
            <span class="text-xs font-black text-slate-700 flex items-center gap-1.5 mt-0.5">
              <span v-if="financialStore.reports.length > 0" class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              <span v-else class="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
              {{ financialStore.reports.length > 0 ? 'Selesai Diekstraksi' : 'Menunggu Dokumen' }}
            </span>
          </div>
        </div>
      </div>

      <!-- Two-tab Layout Sub-Navigation -->
      <div class="flex border-b border-slate-200 bg-white p-1 rounded-xl shadow-xs gap-1 select-none">
        <button 
          @click="activeSubTab = 'competitors'"
          :class="[
            'flex-1 flex items-center justify-center gap-2 py-3 text-xs font-black uppercase tracking-wider rounded-lg transition-all duration-200',
            activeSubTab === 'competitors'
              ? 'bg-emerald-500 text-white shadow-sm'
              : 'text-slate-500 hover:text-slate-800 hover:bg-slate-50'
          ]"
        >
          <Compass class="w-4 h-4" />
          Peta Pasar &amp; Peluang
        </button>
        <button 
          @click="activeSubTab = 'statements'"
          :class="[
            'flex-1 flex items-center justify-center gap-2 py-3 text-xs font-black uppercase tracking-wider rounded-lg transition-all duration-200',
            activeSubTab === 'statements'
              ? 'bg-emerald-500 text-white shadow-sm'
              : 'text-slate-500 hover:text-slate-800 hover:bg-slate-50'
          ]"
        >
          <Landmark class="w-4 h-4" />
          Keuangan &amp; Rekening Koran
        </button>
      </div>

      <!-- Tab Content Area -->
      <div class="transition-opacity duration-200">
        <CompetitorsTab v-if="activeSubTab === 'competitors'" />
        <StatementsTab v-else-if="activeSubTab === 'statements'" />
      </div>

    </div>

  </div>
</template>
