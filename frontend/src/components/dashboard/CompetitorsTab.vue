<script setup lang="ts">
import { ref, computed } from 'vue';
import { useBusinessStore, type Competitor } from '../../stores/business';
import { useFinancialStore } from '../../stores/financial';
import InteractiveMap from './InteractiveMap.vue';
import { 
  Compass, Shield, AlertCircle, Sparkles, AlertTriangle,
  Building, Globe, Trash2, Activity, Landmark
} from 'lucide-vue-next';

const businessStore = useBusinessStore();
const financialStore = useFinancialStore();
const selectedCompetitor = ref<Competitor | null>(null);

function handleSelectCompetitor(comp: Competitor) {
  selectedCompetitor.value = comp;
}

function handleDeselectCompetitor() {
  selectedCompetitor.value = null;
}

// Check if active business has SWOT/sentiment analysis reports loaded
const hasAnalysis = computed(() => {
  const biz = businessStore.activeBusiness;
  if (!biz) return false;
  // If selected competitor is focused, check its analysis
  if (selectedCompetitor.value) {
    return !!(selectedCompetitor.value.competitor_analysis && selectedCompetitor.value.competitor_analysis.length > 0);
  }
  return !!(biz.analysis && biz.analysis.length > 0);
});

// SWOT Data computed values based on focus selection
const activeAnalysis = computed(() => {
  if (selectedCompetitor.value) {
    return selectedCompetitor.value.competitor_analysis?.[0] || null;
  }
  return businessStore.activeBusiness?.analysis?.[0] || null;
});

// Reactive identity details for geospatial & business identity hub
const displayIdentity = computed(() => {
  const biz = businessStore.activeBusiness;
  if (!biz) return null;
  
  if (selectedCompetitor.value) {
    const comp = selectedCompetitor.value;
    return {
      name: comp.name,
      industry: biz.industry,
      address: comp.location.address,
      rating: comp.google_maps_rating || 0,
      numberOfReviews: comp.google_maps_number_of_reviews || 0,
      subdistrict: comp.location.subdistrict,
      city: comp.location.city,
      state: comp.location.state,
      latitude: comp.location.latitude,
      longitude: comp.location.longitude,
      isMainBusiness: false
    };
  }
  
  return {
    name: biz.name,
    industry: biz.industry,
    address: biz.location.address,
    rating: biz.google_maps_rating,
    numberOfReviews: biz.google_maps_number_of_reviews,
    subdistrict: biz.location.subdistrict,
    city: biz.location.city,
    state: biz.location.state,
    latitude: biz.location.latitude,
    longitude: biz.location.longitude,
    isMainBusiness: true
  };
});
</script>

<template>
  <div class="space-y-8 font-sans">
    
    <!-- Empty state: If no business is registered -->
    <div v-if="!businessStore.activeBusiness" class="max-w-2xl mx-auto bg-white rounded-2xl border border-slate-200/80 p-12 text-center shadow-lg relative overflow-hidden select-none">
      <div class="absolute -top-12 -left-12 w-48 h-48 bg-emerald-500/5 blur-3xl rounded-full pointer-events-none"></div>
      <div class="space-y-6 max-w-md mx-auto">
        <div class="w-16 h-16 rounded-2xl bg-slate-50 border border-slate-100 text-slate-400 flex items-center justify-center mx-auto shadow-sm">
          <Compass class="w-8 h-8" />
        </div>
        <h2 class="text-2xl font-black text-slate-800">Menunggu Analisis Pasar</h2>
        <p class="text-sm text-slate-500 font-semibold leading-relaxed">
          Silakan daftarkan bisnis Anda terlebih dahulu untuk membuka pemetaan pasar geospasial dan SWOT kompetitor.
        </p>
      </div>
    </div>

    <!-- Active State: Market Mapping & SWOT Dashboard -->
    <div v-else class="space-y-8">
      
      <!-- Top HUD Header banner -->
      <div class="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-sm flex flex-wrap items-center justify-between gap-4 select-none">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-emerald-50 border border-emerald-100 flex items-center justify-center text-emerald-600 shadow-sm shrink-0">
            <Compass class="w-5.5 h-5.5" />
          </div>
          <div>
            <h3 class="text-base font-extrabold text-slate-800">Pemetaan Kompetitor &amp; Geospasial</h3>
            <p class="text-xs text-slate-550 font-bold">Analisis intelijen pasar terdekat bersumber dari ulasan digital Google Maps</p>
          </div>
        </div>
        
        <div class="flex items-center gap-2">
          <span class="text-xs font-bold text-slate-500">Fokus Analisis:</span>
          <span class="badge bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-black uppercase tracking-wider px-3 py-2">
            {{ selectedCompetitor ? selectedCompetitor.name : 'Bisnis Utama' }}
          </span>
          <button 
            v-if="selectedCompetitor" 
            @click="handleDeselectCompetitor" 
            class="btn btn-xs bg-slate-50 hover:bg-slate-100 border border-slate-200 hover:border-slate-300 text-slate-650 rounded-lg font-black ml-2"
          >
            Reset ke Bisnis Utama
          </button>
        </div>
      </div>

      <!-- Main Columns Layout -->
      <div class="grid grid-cols-1 xl:grid-cols-12 gap-8 items-start">
        
        <!-- Left: Interactive Geolocation Map (7 cols) -->
        <div class="xl:col-span-7 2xl:col-span-8 space-y-6">
          <InteractiveMap 
            :business="businessStore.activeBusiness"
            :competitors="businessStore.competitors"
            :selectedCompetitorId="selectedCompetitor?.id || null"
            @select-competitor="handleSelectCompetitor"
            @deselect="handleDeselectCompetitor"
          />

          <!-- Premium Detail Information Panel (Geospatial & Business Identity Hub) -->
          <div v-if="displayIdentity" class="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-md space-y-6 animate-fade-in">
            <div class="flex items-center justify-between border-b border-slate-100 pb-5 flex-wrap gap-4 select-none">
              <div class="flex items-center gap-4">
                <div class="w-12 h-12 rounded-xl bg-emerald-50 border border-emerald-100 flex items-center justify-center text-emerald-600 shadow-sm shrink-0">
                  <Building class="w-6 h-6" />
                </div>
                <div>
                  <div class="flex items-center gap-2">
                    <h2 class="text-xl font-extrabold text-slate-800">{{ displayIdentity.name }}</h2>
                    <span class="badge bg-emerald-50 border border-emerald-200 text-emerald-700 text-[9.5px] font-black uppercase tracking-wider px-2 py-1 rounded-md">
                      {{ displayIdentity.industry }}
                    </span>
                  </div>
                  <p class="text-xs text-slate-550 font-bold mt-1.5 flex items-center gap-1">
                    <Globe class="w-3.5 h-3.5 text-slate-400" />
                    {{ displayIdentity.address }}
                  </p>
                </div>
              </div>

              <div>
                <button 
                  v-if="displayIdentity.isMainBusiness" 
                  @click="businessStore.deleteBusiness" 
                  class="btn btn-outline btn-error btn-xs border rounded-lg text-xs font-bold gap-1 px-3"
                >
                  <Trash2 class="w-3.5 h-3.5" /> Hapus Bisnis
                </button>
                <span 
                  v-else 
                  class="badge bg-amber-50 border border-amber-200 text-amber-800 text-[10px] font-black uppercase tracking-wider px-2.5 py-1.5 rounded-md"
                >
                  Fokus Kompetitor
                </span>
              </div>
            </div>

            <!-- Metric Grid -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-6 font-sans">
              <div class="bg-slate-50 border border-slate-100 p-5 rounded-xl text-center">
                <span class="text-[10px] font-extrabold text-slate-550 uppercase tracking-wider block">Rating Google Maps</span>
                <span class="text-2xl font-black text-slate-800 mt-2 block">
                  ★ {{ displayIdentity.rating }}
                </span>
              </div>

              <div class="bg-slate-50 border border-slate-100 p-5 rounded-xl text-center">
                <span class="text-[10px] font-extrabold text-slate-550 uppercase tracking-wider block">Review Terindeks</span>
                <span class="text-2xl font-black text-slate-800 mt-2 block">
                  {{ displayIdentity.numberOfReviews }}
                </span>
              </div>

              <div class="bg-slate-50 border border-slate-100 p-5 rounded-xl text-center">
                <span class="text-[10px] font-extrabold text-slate-550 uppercase tracking-wider block">Kecamatan / Wilayah</span>
                <span class="text-sm font-black text-slate-800 mt-3 truncate block uppercase font-mono">
                  {{ displayIdentity.subdistrict }}, {{ displayIdentity.city.split(' ')[0] }}
                </span>
              </div>
            </div>

            <!-- Additional Geolocation Card details -->
            <div class="bg-slate-50 border border-slate-100 rounded-xl p-5 font-sans space-y-4">
              <h4 class="text-xs font-black text-slate-850 uppercase tracking-wider flex items-center gap-1.5 select-none">
                <Globe class="w-4 h-4 text-slate-500" />
                Detail Geospasial Geokode
              </h4>
              
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs font-semibold text-slate-600">
                <div>
                  <span class="text-[11px] text-slate-550 font-black block">Kota</span>
                  <span class="text-slate-800 font-bold block mt-0.5">{{ displayIdentity.city }}</span>
                </div>
                <div>
                  <span class="text-[11px] text-slate-550 font-black block">Provinsi</span>
                  <span class="text-slate-800 font-bold block mt-0.5">{{ displayIdentity.state }}</span>
                </div>
                <div>
                  <span class="text-[11px] text-slate-550 font-black block">Garis Lintang (Lat)</span>
                  <span class="text-slate-800 font-mono block mt-0.5">{{ displayIdentity.latitude.toFixed(6) }}</span>
                </div>
                <div>
                  <span class="text-[11px] text-slate-550 font-black block">Garis Bujur (Lng)</span>
                  <span class="text-slate-800 font-mono block mt-0.5">{{ displayIdentity.longitude.toFixed(6) }}</span>
                </div>
              </div>
            </div>

            <!-- Nearby Competitors Micro-Table List (Fix #2 to fill empty space and balance columns) -->
            <div class="bg-slate-50 border border-slate-100 rounded-xl p-5 font-sans space-y-3">
              <div class="flex items-center justify-between select-none">
                <h4 class="text-xs font-black text-slate-850 uppercase tracking-wider flex items-center gap-1.5">
                  <Building class="w-4 h-4 text-emerald-600" />
                  Daftar Kompetitor Terdekat
                </h4>
                <span class="text-[9px] bg-emerald-50 border border-emerald-200 text-emerald-800 px-2 py-0.5 rounded font-black uppercase tracking-wider">
                  {{ businessStore.competitors.length }} Terdeteksi
                </span>
              </div>
              
              <div class="overflow-x-auto">
                <table class="table table-sm w-full text-[11px] text-slate-650">
                  <thead>
                    <tr class="text-slate-400 text-[9px] font-black uppercase tracking-wider border-b border-slate-200 select-none">
                      <th class="py-2 text-left pl-0">Nama Bisnis</th>
                      <th class="py-2 text-center">Kategori</th>
                      <th class="py-2 text-center">Jarak</th>
                      <th class="py-2 text-right pr-0">Rating</th>
                    </tr>
                  </thead>
                  <tbody class="font-semibold">
                    <tr 
                      v-for="comp in businessStore.competitors" 
                      :key="comp.id"
                      @click="handleSelectCompetitor(comp)"
                      :class="[
                        'border-b border-slate-100/50 hover:bg-white/80 cursor-pointer transition-colors duration-150',
                        selectedCompetitor?.id === comp.id ? 'bg-emerald-50/50 hover:bg-emerald-50' : ''
                      ]"
                    >
                      <td class="py-2 pl-0 font-bold text-slate-800">
                        <div class="flex items-center gap-2">
                          <span :class="['w-2 h-2 rounded-full shrink-0', comp.competitor_type === 'Direct' ? 'bg-rose-500' : 'bg-amber-500']"></span>
                          <span class="truncate max-w-[150px]">{{ comp.name }}</span>
                        </div>
                      </td>
                      <td class="py-2 text-center">
                        <span :class="[
                          'badge badge-xs text-[8px] font-black uppercase tracking-wider px-2 py-0.5 rounded',
                          comp.competitor_type === 'Direct' ? 'bg-rose-50 border-rose-200 text-rose-700' : 'bg-amber-50 border-amber-200 text-amber-850'
                        ]">
                          {{ comp.competitor_type }}
                        </span>
                      </td>
                      <td class="py-2 text-center font-mono text-slate-550 text-[10px]">
                        {{ comp.id === 'comp_01' ? '350m' : (comp.id === 'comp_02' ? '520m' : '220m') }}
                      </td>
                      <td class="py-2 text-right font-black pr-0 text-slate-800">
                        ★ {{ comp.google_maps_rating }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Connection Asset Indicator HUD -->
            <div class="border border-slate-100 rounded-xl p-5 flex flex-wrap items-center justify-between gap-4 font-sans select-none">
              <div class="flex items-center gap-3">
                <Activity class="w-5 h-5 text-emerald-500" />
                <div>
                  <h4 class="text-xs font-black text-slate-800 uppercase tracking-wider">Status Integrasi Hub Vantage AI</h4>
                  <p class="text-[10px] text-slate-550 font-bold">Memantau ketersediaan asset geospasial dan audit finansial Anda</p>
                </div>
              </div>
              <div class="flex gap-3">
                <span class="flex items-center gap-1 bg-slate-50 border border-slate-200 text-slate-650 text-[10px] font-black uppercase tracking-wider px-2.5 py-1 rounded-md">
                  <Compass class="w-3.5 h-3.5 text-slate-400" />
                  Radar: 3 Nodes
                </span>
                <span class="flex items-center gap-1 bg-slate-50 border border-slate-200 text-slate-650 text-[10px] font-black uppercase tracking-wider px-2.5 py-1 rounded-md">
                  <Landmark class="w-3.5 h-3.5 text-slate-400" />
                  Kas: {{ financialStore.reports.length }} Connected
                </span>
              </div>
            </div>

          </div>
        </div>

        <!-- Right: Focused Sentiment Summary (5 cols) -->
        <div class="xl:col-span-5 2xl:col-span-4 bg-white rounded-2xl border border-slate-200/80 p-6 shadow-md min-h-[460px] flex flex-col justify-between">
          <div v-if="hasAnalysis" class="space-y-5">
            <div class="border-b border-slate-100 pb-3 select-none">
              <span class="text-[9px] font-black text-slate-400 uppercase tracking-widest block">Ringkasan Fokus</span>
              <h4 class="text-md font-black text-slate-800 truncate mt-0.5">
                {{ selectedCompetitor ? selectedCompetitor.name : businessStore.activeBusiness.name }}
              </h4>
            </div>

            <div class="bg-slate-50 border border-slate-100 p-4 rounded-xl space-y-1">
              <div class="flex items-center gap-1.5 select-none">
                <Sparkles class="w-4 h-4 text-emerald-600 animate-pulse" />
                <span class="text-[9px] font-black text-slate-550 uppercase tracking-wider block">Sentimen Umum AI</span>
              </div>
              <p class="text-xs text-slate-700 font-semibold leading-relaxed mt-1">
                {{ activeAnalysis?.sentiment }}
              </p>
            </div>

            <!-- Sentiment Ratio Micro-Bar Chart -->
            <div v-if="activeAnalysis?.top_positive_reviews?.length || activeAnalysis?.top_negative_reviews?.length" class="bg-slate-50 border border-slate-100 p-4 rounded-xl space-y-2 select-none">
              <div class="flex items-center justify-between text-[9px] font-black uppercase tracking-wider text-slate-550">
                <span>Rasio Sentimen Konsumen</span>
                <span class="text-emerald-700 font-black">
                  {{ Math.round((activeAnalysis.top_positive_reviews.length / (activeAnalysis.top_positive_reviews.length + activeAnalysis.top_negative_reviews.length)) * 100) }}% Positif
                </span>
              </div>
              <div class="w-full h-2.5 bg-rose-200/60 rounded-full overflow-hidden flex">
                <div 
                  class="h-full bg-emerald-500 transition-all duration-500" 
                  :style="{ width: `${(activeAnalysis.top_positive_reviews.length / (activeAnalysis.top_positive_reviews.length + activeAnalysis.top_negative_reviews.length)) * 100}%` }"
                ></div>
              </div>
              <div class="flex items-center justify-between text-[8.5px] text-slate-500 font-extrabold">
                <span class="flex items-center gap-1 text-emerald-600">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                  {{ activeAnalysis.top_positive_reviews.length }} Aspek Positif
                </span>
                <span class="flex items-center gap-1 text-rose-500">
                  <span class="w-1.5 h-1.5 rounded-full bg-rose-500"></span>
                  {{ activeAnalysis.top_negative_reviews.length }} Aspek Negatif
                </span>
              </div>
            </div>

            <!-- Categorized Reviews Grouped Block -->
            <div class="space-y-4">
              <span class="text-[9px] font-black text-slate-500 uppercase tracking-widest block select-none">Ulasan Konsumen Terperinci</span>
              
              <!-- Aspek Positif Terkemuka -->
              <div v-if="activeAnalysis?.top_positive_reviews?.length" class="space-y-2">
                <div class="flex items-center justify-between border-b border-slate-100 pb-1.5 select-none">
                  <span class="text-[10px] font-extrabold text-emerald-700 flex items-center gap-1">
                    <Shield class="w-3.5 h-3.5 shrink-0" />
                    Aspek Positif Terkemuka
                  </span>
                  <span class="text-[8px] bg-emerald-100 border border-emerald-200 text-emerald-800 px-1.5 py-0.5 rounded font-black uppercase tracking-wider shrink-0">Positif</span>
                </div>
                <div class="space-y-2">
                  <div 
                    v-for="(rev, i) in activeAnalysis.top_positive_reviews"
                    :key="'rev-'+i"
                    class="bg-emerald-50/25 border border-emerald-100/40 p-3 rounded-xl flex gap-2.5 items-start text-xs font-semibold text-emerald-950/80 leading-relaxed"
                  >
                    <span class="text-emerald-500 font-black text-[9px] mt-0.5">#{{ i + 1 }}</span>
                    <span>{{ rev }}</span>
                  </div>
                </div>
              </div>

              <!-- Aspek Negatif / Hambatan -->
              <div v-if="activeAnalysis?.top_negative_reviews?.length" class="space-y-2">
                <div class="flex items-center justify-between border-b border-slate-100 pb-1.5 select-none">
                  <span class="text-[10px] font-extrabold text-rose-700 flex items-center gap-1">
                    <AlertCircle class="w-3.5 h-3.5 shrink-0" />
                    Aspek Negatif / Hambatan
                  </span>
                  <span class="text-[8px] bg-rose-100 border border-rose-200 text-rose-800 px-1.5 py-0.5 rounded font-black uppercase tracking-wider shrink-0">Hambatan</span>
                </div>
                <div class="space-y-2">
                  <div 
                    v-for="(rev, i) in activeAnalysis.top_negative_reviews"
                    :key="'rev-neg-'+i"
                    class="bg-rose-50/25 border border-rose-100/40 p-3 rounded-xl flex gap-2.5 items-start text-xs font-semibold text-rose-950/80 leading-relaxed"
                  >
                    <span class="text-rose-400 font-black text-[9px] mt-0.5">#{{ i + 1 }}</span>
                    <span>{{ rev }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Placeholder Inside Right Tab if empty/no-data -->
          <div v-else class="flex-1 flex flex-col items-center justify-center text-center p-8 select-none">
            <div class="w-12 h-12 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-center text-slate-400 mb-3">
              <Sparkles class="w-6 h-6 animate-pulse text-emerald-500" />
            </div>
            <h4 class="text-sm font-black text-slate-800">Menghitung Sentimen...</h4>
            <p class="text-xs text-slate-400 font-medium mt-1 leading-relaxed">
              Analisis sentimen berbasis kecerdasan buatan sedang dikonfigurasi untuk lokasi geospasial ini.
            </p>
          </div>

          <div class="pt-4 text-center text-[10px] text-slate-550 font-extrabold uppercase tracking-widest select-none border-t border-slate-100 mt-4">
            Gunakan radar di kiri untuk berpindah fokus
          </div>
        </div>

      </div>

      <!-- Professional Expanded 4-Quadrant SWOT Matrix (Fills entire row width) -->
      <div class="bg-white rounded-2xl border border-slate-200/80 p-6 md:p-8 shadow-md space-y-6">
        <div class="select-none">
          <span class="text-[9px] font-black text-slate-400 uppercase tracking-widest block">Metrik Analisis Bisnis</span>
          <h3 class="text-base font-extrabold text-slate-800 mt-0.5">Struktur Diagnostik Operasional &amp; Pasar</h3>
        </div>

        <div v-if="hasAnalysis && activeAnalysis" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 font-sans">
          <!-- Kelebihan Utama (Emerald) -->
          <div class="bg-emerald-50/20 border border-emerald-100 rounded-2xl p-5 flex flex-col justify-between">
            <div class="space-y-4">
              <div class="bg-emerald-500/10 border-b border-emerald-100 -mx-5 -mt-5 px-5 py-4 mb-4 rounded-t-2xl flex items-center justify-between select-none">
                <div class="flex items-center gap-2 text-emerald-850 font-black text-xs uppercase tracking-wider">
                  <Shield class="w-4.5 h-4.5 text-emerald-600" />
                  Kelebihan Utama
                </div>
              </div>
              <ul class="text-xs text-emerald-950/80 font-semibold space-y-3 leading-relaxed">
                <li 
                  v-for="(st, i) in activeAnalysis.strengths"
                  :key="'st-'+i"
                  class="flex gap-2 items-start justify-between"
                >
                  <div class="flex gap-2 items-start">
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 shrink-0 mt-1.5"></span>
                    <span>{{ st }}</span>
                  </div>
                  <span v-if="i === 0" class="badge badge-xs bg-emerald-100 border border-emerald-200 text-emerald-700 text-[8px] font-black uppercase tracking-wider py-1 px-1.5 rounded ml-2 shrink-0 select-none">Utama</span>
                </li>
              </ul>
            </div>
          </div>

          <!-- Area Perbaikan (Rose) -->
          <div class="bg-rose-50/20 border border-rose-100 rounded-2xl p-5 flex flex-col justify-between">
            <div class="space-y-4">
              <div class="bg-rose-500/10 border-b border-rose-100 -mx-5 -mt-5 px-5 py-4 mb-4 rounded-t-2xl flex items-center justify-between select-none">
                <div class="flex items-center gap-2 text-rose-850 font-black text-xs uppercase tracking-wider">
                  <AlertCircle class="w-4.5 h-4.5 text-rose-600" />
                  Area Perbaikan
                </div>
              </div>
              <ul class="text-xs text-rose-950/80 font-semibold space-y-3 leading-relaxed">
                <li 
                  v-for="(wk, i) in activeAnalysis.weaknesses"
                  :key="'wk-'+i"
                  class="flex gap-2 items-start justify-between"
                >
                  <div class="flex gap-2 items-start">
                    <span class="w-1.5 h-1.5 rounded-full bg-rose-500 shrink-0 mt-1.5"></span>
                    <span>{{ wk }}</span>
                  </div>
                  <span v-if="i === 0" class="badge badge-xs bg-rose-100 border border-rose-200 text-rose-700 text-[8px] font-black uppercase tracking-wider py-1 px-1.5 rounded ml-2 shrink-0 select-none animate-pulse">Kritis</span>
                </li>
              </ul>
            </div>
          </div>

          <!-- Peluang Pertumbuhan (Sky) -->
          <div class="bg-sky-50/20 border border-sky-100 rounded-2xl p-5 flex flex-col justify-between">
            <div class="space-y-4">
              <div class="bg-sky-500/10 border-b border-sky-100 -mx-5 -mt-5 px-5 py-4 mb-4 rounded-t-2xl flex items-center justify-between select-none">
                <div class="flex items-center gap-2 text-sky-850 font-black text-xs uppercase tracking-wider">
                  <Sparkles class="w-4.5 h-4.5 text-sky-600" />
                  Peluang Pertumbuhan
                </div>
              </div>
              <ul class="text-xs text-sky-950/80 font-semibold space-y-3 leading-relaxed">
                <li 
                  v-for="(op, i) in activeAnalysis.opportunities"
                  :key="'op-'+i"
                  class="flex gap-2 items-start justify-between"
                >
                  <div class="flex gap-2 items-start">
                    <span class="w-1.5 h-1.5 rounded-full bg-sky-500 shrink-0 mt-1.5"></span>
                    <span>{{ op }}</span>
                  </div>
                  <span v-if="i === 0" class="badge badge-xs bg-sky-100 border border-sky-200 text-sky-700 text-[8px] font-black uppercase tracking-wider py-1 px-1.5 rounded ml-2 shrink-0 select-none">Prospek</span>
                </li>
              </ul>
            </div>
          </div>

          <!-- Tantangan Pasar (Amber) -->
          <div class="bg-amber-50/20 border border-amber-100 rounded-2xl p-5 flex flex-col justify-between">
            <div class="space-y-4">
              <div class="bg-amber-500/10 border-b border-amber-100 -mx-5 -mt-5 px-5 py-4 mb-4 rounded-t-2xl flex items-center justify-between select-none">
                <div class="flex items-center gap-2 text-amber-850 font-black text-xs uppercase tracking-wider">
                  <AlertTriangle class="w-4.5 h-4.5 text-amber-600" />
                  Tantangan Pasar
                </div>
              </div>
              <ul class="text-xs text-amber-950/80 font-semibold space-y-3 leading-relaxed">
                <li 
                  v-for="(th, i) in activeAnalysis.threats"
                  :key="'th-'+i"
                  class="flex gap-2 items-start justify-between"
                >
                  <div class="flex gap-2 items-start">
                    <span class="w-1.5 h-1.5 rounded-full bg-amber-500 shrink-0 mt-1.5"></span>
                    <span>{{ th }}</span>
                  </div>
                  <span v-if="i === 0" class="badge badge-xs bg-amber-100 border border-amber-200 text-amber-800 text-[8px] font-black uppercase tracking-wider py-1 px-1.5 rounded ml-2 shrink-0 select-none animate-pulse">Penting</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- No SWOT Analysis data placeholder -->
        <div v-else class="py-12 text-center select-none">
          <div class="w-14 h-14 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-center text-slate-400 mx-auto mb-4">
            <Sparkles class="w-6 h-6 animate-pulse text-emerald-500" />
          </div>
          <h4 class="text-md font-black text-slate-800">Menyusun Matriks Diagnostik Bisnis...</h4>
          <p class="text-xs text-slate-500 font-semibold mt-1 max-w-sm mx-auto leading-relaxed">
            Data geokode pasar dan ulasan konsumen sedang disintesis ke dalam diagram diagnostik bisnis terstruktur.
          </p>
        </div>

      </div>

    </div>

  </div>
</template>
