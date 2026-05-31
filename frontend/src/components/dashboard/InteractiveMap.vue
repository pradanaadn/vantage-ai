<script setup lang="ts">
import { ref, computed } from 'vue';
import { type Competitor, type Business } from '../../stores/business';
import { ZoomIn, ZoomOut, Layers } from 'lucide-vue-next';

const props = defineProps<{
  business: Business | null;
  competitors: Competitor[];
  selectedCompetitorId: string | null;
}>();

const emit = defineEmits<{
  (e: 'select-competitor', competitor: Competitor): void;
  (e: 'deselect'): void;
}>();

// Map bounds and view state
const mapZoom = ref(1.1);
const showGrid = ref(true);
const showTerrain = ref(true);

// Toggle filter states for map coordinates
const visibleCategories = ref({
  primary: true,
  direct: true,
  indirect: true
});

// Convert lat/long coordinates to simple local SVG coordinate spaces (0 - 500 px)
const mapCoordinates = computed(() => {
  if (!props.business) return [];

  // Default coordinate center
  const centerLat = props.business.location.latitude;
  const centerLng = props.business.location.longitude;

  const scale = 25000; // Multiplier to spread coordinates

  const businessX = 250;
  const businessY = 200;

  return props.competitors
    .filter(c => {
      if (c.competitor_type === 'Direct' && !visibleCategories.value.direct) return false;
      if (c.competitor_type === 'Indirect' && !visibleCategories.value.indirect) return false;
      return true;
    })
    .map(c => {
      const dx = (c.location.longitude - centerLng) * scale;
      const dy = (c.location.latitude - centerLat) * scale;

      return {
        ...c,
        x: businessX + dx,
        y: businessY - dy
      };
    });
});

function handleNodeClick(comp: Competitor) {
  emit('select-competitor', comp);
}

function handleBaseClick() {
  emit('deselect');
}

function zoomIn() {
  if (mapZoom.value < 1.8) mapZoom.value += 0.15;
}

function zoomOut() {
  if (mapZoom.value > 0.6) mapZoom.value -= 0.15;
}
</script>

<template>
  <div class="relative bg-sky-50/30 rounded-2xl border border-slate-200/80 overflow-hidden shadow-md flex flex-col min-h-[460px] w-full">
    <!-- Grid decorative background - Light Mode Blueprint style -->
    <div class="absolute inset-0 bg-[radial-gradient(#0284c7_1px,transparent_1px)] [background-size:16px_16px] pointer-events-none opacity-[0.09]"></div>

    <!-- Map Title & Status HUD overlay - Light Theme -->
    <div class="absolute top-4 left-4 z-10 bg-white/95 backdrop-blur-md border border-slate-200 px-4 py-2.5 rounded-xl flex flex-col gap-0.5 shadow-sm select-none">
      <div class="flex items-center gap-2 text-[10px] font-black tracking-widest text-emerald-600 uppercase">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
        Radar Geospasial Pasar
      </div>
      <div class="text-[9px] text-slate-500 font-mono tracking-wider font-semibold">
        Lat: {{ business?.location.latitude.toFixed(4) || '0' }}, Lng: {{ business?.location.longitude.toFixed(4) || '0' }}
      </div>
    </div>

    <!-- Map Utility Controls - Standardized vertical control block on the side -->
    <div class="absolute top-1/2 -translate-y-1/2 right-4 z-10 flex flex-col gap-2 select-none bg-white/95 backdrop-blur-md border border-slate-200 p-1.5 rounded-xl shadow-md">
      <button @click="zoomIn" class="btn btn-square btn-xs bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-650 rounded-lg shadow-sm" title="Perbesar">
        <ZoomIn class="w-3.5 h-3.5" />
      </button>
      <button @click="zoomOut" class="btn btn-square btn-xs bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-650 rounded-lg shadow-sm" title="Perkecil">
        <ZoomOut class="w-3.5 h-3.5" />
      </button>
      <div class="border-t border-slate-150 my-0.5"></div>
      <button @click="showGrid = !showGrid" :class="['btn btn-square btn-xs border rounded-lg shadow-sm', showGrid ? 'bg-sky-50 border-sky-200 text-sky-600 hover:bg-sky-100' : 'bg-slate-50 text-slate-550 border-slate-200 hover:bg-slate-100']" title="Toggle Garis Kisi">
        <Layers class="w-3.5 h-3.5" />
      </button>
    </div>

    <!-- Interactive Canvas SVG -->
    <div class="flex-1 w-full relative min-h-[380px] overflow-hidden flex items-center justify-center cursor-grab active:cursor-grabbing" @click.self="handleBaseClick">
      
      <svg 
        viewBox="0 0 500 400" 
        class="w-full h-full max-h-[420px] transition-transform duration-300 ease-out select-none"
        :style="{ transform: `scale(${mapZoom})` }"
        @click.self="handleBaseClick"
      >
        <!-- Terrain / Rivers representation (Light Theme Blueprint Style) -->
        <g v-if="showTerrain" opacity="0.3">
          <path d="M-50,80 Q 150,120 220,180 T 400,240 T 550,290" fill="none" stroke="#38bdf8" stroke-width="16" stroke-linecap="round" opacity="0.15" />
          <path d="M-50,80 Q 150,120 220,180 T 400,240 T 550,290" fill="none" stroke="#0ea5e9" stroke-width="4" stroke-linecap="round" opacity="0.3" />
          
          <rect x="50" y="240" width="100" height="90" rx="16" fill="#10b981" opacity="0.05" />
          <circle cx="420" cy="90" r="50" fill="#10b981" opacity="0.05" />
        </g>

        <!-- Dynamic Grid lines - Blue Blueprint theme -->
        <g v-if="showGrid" stroke="#0284c7" stroke-width="0.3" opacity="0.12">
          <line v-for="i in 10" :key="'h'+i" x1="0" :y1="i * 40" x2="500" :y2="i * 40" />
          <line v-for="i in 12" :key="'v'+i" :x1="i * 40" y1="0" :x2="i * 40" y2="400" />
        </g>

        <!-- Radar Pulse rings with Faint Scale Distance Labels centering on Active Business -->
        <g v-if="business && visibleCategories.primary">
          <!-- 250m ring -->
          <circle cx="250" cy="200" r="60" fill="none" stroke="#10b981" stroke-width="0.75" opacity="0.22" stroke-dasharray="4 4" />
          <text x="250" y="136" fill="#047857" opacity="0.5" font-size="7" font-weight="extrabold" text-anchor="middle" font-family="sans-serif">250 m</text>
          
          <!-- 500m ring -->
          <circle cx="250" cy="200" r="130" fill="none" stroke="#10b981" stroke-width="0.5" opacity="0.15" />
          <text x="250" y="66" fill="#047857" opacity="0.45" font-size="7" font-weight="extrabold" text-anchor="middle" font-family="sans-serif">500 m</text>
          
          <!-- 1km ring -->
          <circle cx="250" cy="200" r="200" fill="none" stroke="#10b981" stroke-width="0.5" opacity="0.08" stroke-dasharray="8 8" />
          <text x="250" y="10" fill="#047857" opacity="0.4" font-size="7" font-weight="extrabold" text-anchor="middle" font-family="sans-serif">1 km</text>
        </g>

        <!-- Connecting lines from Business to Competitors -->
        <g stroke="#94a3b8" stroke-width="1" stroke-dasharray="2 2" opacity="0.6" v-if="business && visibleCategories.primary">
          <line 
            v-for="comp in mapCoordinates" 
            :key="'line-'+comp.id"
            x1="250" 
            y1="200" 
            :x2="comp.x" 
            :y2="comp.y"
            :stroke="selectedCompetitorId === comp.id ? '#f43f5e' : '#0284c7'"
            :stroke-width="selectedCompetitorId === comp.id ? '1.5' : '1'"
            :opacity="selectedCompetitorId === comp.id ? '0.8' : '0.4'"
          />
        </g>

        <!-- Competitor Markers -->
        <g v-for="comp in mapCoordinates" :key="comp.id" class="cursor-pointer group/node" @click="handleNodeClick(comp)">
          
          <!-- Native SVG Pulse rings centering precisely on Competitor coordinate (cx, cy) - Bound to Vue :key -->
          <circle 
            v-if="selectedCompetitorId === comp.id"
            :key="'pulse-' + comp.id"
            :cx="comp.x" 
            :cy="comp.y" 
            r="6" 
            fill="none" 
            stroke="#f43f5e" 
            stroke-width="1.5" 
            opacity="0.8"
          >
            <animate attributeName="r" values="6;22" dur="2s" repeatCount="indefinite" />
            <animate attributeName="opacity" values="0.8;0" dur="2s" repeatCount="indefinite" />
          </circle>

          <!-- Pin Base Glow -->
          <circle 
            :cx="comp.x" 
            :cy="comp.y" 
            :r="selectedCompetitorId === comp.id ? 8 : 6" 
            :fill="comp.competitor_type === 'Direct' ? '#f43f5e' : '#f59e0b'" 
            opacity="0.25"
            class="transition-all duration-300"
          />

          <!-- Sleek Location Pin Teardrop Vector Shape instead of Emoji -->
          <path 
            :d="`M ${comp.x},${comp.y} C ${comp.x - 6},${comp.y - 6} ${comp.x - 6},${comp.y - 14} ${comp.x},${comp.y - 15} C ${comp.x + 6},${comp.y - 14} ${comp.x + 6},${comp.y - 6} ${comp.x},${comp.y} Z`" 
            :fill="comp.competitor_type === 'Direct' ? '#e11d48' : '#d97706'"
            stroke="#ffffff"
            stroke-width="0.8"
            class="transition-all duration-300"
          />
          
          <!-- Pin Center Dot -->
          <circle 
            :cx="comp.x" 
            :cy="comp.y - 10" 
            r="2" 
            fill="#ffffff" 
          />

          <!-- Label Hover tooltip -->
          <g class="opacity-90 group-hover/node:opacity-100 transition-opacity duration-300">
            <rect 
              :x="comp.x - 50" 
              :y="comp.y - 32" 
              width="100" 
              height="16" 
              rx="4" 
              fill="#ffffff" 
              stroke="#cbd5e1" 
              stroke-width="0.75" 
              opacity="0.95" 
            />
            <text 
              :x="comp.x" 
              :y="comp.y - 21" 
              fill="#334155" 
              font-size="8" 
              font-family="sans-serif" 
              text-anchor="middle"
              font-weight="bold"
            >
              {{ comp.name.split(' ')[0] }} ({{ comp.google_maps_rating }})
            </text>
          </g>
        </g>

        <!-- Primary Target Business Pin (Kopi Nusantara) -->
        <g v-if="business && visibleCategories.primary" class="cursor-pointer" @click="handleBaseClick">
          <!-- Native SVG Pulse rings for business - Bound to Vue :key -->
          <circle :key="'primary-pulse-' + business.id" cx="250" cy="200" r="8" fill="none" stroke="#10b981" stroke-width="2" opacity="0.6">
            <animate attributeName="r" values="8;28" dur="2.4s" repeatCount="indefinite" />
            <animate attributeName="opacity" values="0.6;0" dur="2.4s" repeatCount="indefinite" />
          </circle>
          
          <!-- Premium Teardrop Pin Shape in emerald -->
          <path 
            d="M 250,200 C 242,192 240,182 250,180 C 260,182 258,192 250,200 Z" 
            fill="#059669" 
            stroke="#ffffff" 
            stroke-width="1.2" 
          />
          <circle cx="250" cy="189" r="3.2" fill="#ffffff" />
          
          <!-- Primary Business Tooltip Label -->
          <g>
            <rect x="180" y="150" width="140" height="20" rx="6" fill="#f0fdf4" stroke="#86efac" stroke-width="1.2" />
            <text x="250" y="163" fill="#166534" font-size="8.5" font-weight="black" text-anchor="middle" font-family="sans-serif">
              {{ business.name }}
            </text>
          </g>
        </g>
      </svg>
    </div>

    <!-- Map Legends Footer - Light Theme with Interactive Filters -->
    <div class="bg-white border-t border-slate-200/80 px-6 py-4.5 flex flex-wrap items-center justify-between gap-4 text-[11px] select-none text-slate-500">
      <div class="flex items-center gap-5 flex-wrap">
        <div 
          @click="visibleCategories.primary = !visibleCategories.primary" 
          class="flex items-center gap-2 cursor-pointer select-none transition-all duration-250 hover:text-emerald-700"
          :class="{ 'opacity-35 hover:opacity-75': !visibleCategories.primary }"
        >
          <svg class="w-2.5 h-2.5 text-emerald-500" viewBox="0 0 10 10" fill="currentColor">
            <circle cx="5" cy="5" r="4" stroke="white" stroke-width="1"/>
          </svg>
          <span class="font-bold">Bisnis Utama</span>
          <span class="text-[8px] bg-slate-100 text-slate-450 px-1.5 py-0.5 rounded-md uppercase font-black tracking-wider ml-1">
            {{ visibleCategories.primary ? 'Aktif' : 'Sembunyi' }}
          </span>
        </div>

        <div 
          @click="visibleCategories.direct = !visibleCategories.direct" 
          class="flex items-center gap-2 cursor-pointer select-none transition-all duration-250 hover:text-rose-700"
          :class="{ 'opacity-35 hover:opacity-75': !visibleCategories.direct }"
        >
          <svg class="w-2.5 h-2.5 text-rose-500" viewBox="0 0 10 10" fill="currentColor">
            <circle cx="5" cy="5" r="4" stroke="white" stroke-width="1"/>
          </svg>
          <span class="font-bold">Kompetitor Langsung</span>
          <span class="text-[8px] bg-slate-100 text-slate-450 px-1.5 py-0.5 rounded-md uppercase font-black tracking-wider ml-1">
            {{ visibleCategories.direct ? 'Aktif' : 'Sembunyi' }}
          </span>
        </div>

        <div 
          @click="visibleCategories.indirect = !visibleCategories.indirect" 
          class="flex items-center gap-2 cursor-pointer select-none transition-all duration-250 hover:text-amber-700"
          :class="{ 'opacity-35 hover:opacity-75': !visibleCategories.indirect }"
        >
          <svg class="w-2.5 h-2.5 text-amber-500" viewBox="0 0 10 10" fill="currentColor">
            <circle cx="5" cy="5" r="4" stroke="white" stroke-width="1"/>
          </svg>
          <span class="font-bold">Kompetitor Tidak Langsung</span>
          <span class="text-[8px] bg-slate-100 text-slate-450 px-1.5 py-0.5 rounded-md uppercase font-black tracking-wider ml-1">
            {{ visibleCategories.indirect ? 'Aktif' : 'Sembunyi' }}
          </span>
        </div>
      </div>
      <div class="text-slate-400 font-mono text-[9px]">
        Klik item legenda di atas untuk menyembunyikan/menampilkan pin radar
      </div>
    </div>
  </div>
</template>
