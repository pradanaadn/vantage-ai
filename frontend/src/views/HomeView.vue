<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useBusinessStore } from '../stores/business';
import { useFinancialStore } from '../stores/financial';
import { useRouter } from 'vue-router';
import BusinessTab from '../components/dashboard/BusinessTab.vue';
import FinancialTab from '../components/dashboard/FinancialTab.vue';
import ProfileTab from '../components/dashboard/ProfileTab.vue';
import VantageLogo from '../components/base/VantageLogo.vue';
import { 
  Building, Landmark, User, LogOut, Compass, 
  Menu, X, Sparkles, Activity, FileText, ChevronRight 
} from 'lucide-vue-next';

const authStore = useAuthStore();
const businessStore = useBusinessStore();
const financialStore = useFinancialStore();
const router = useRouter();

// Tab state: 'business' | 'financial' | 'profile'
const activeTab = ref<'business' | 'financial' | 'profile'>('business');
const isMobileSidebarOpen = ref(false);

onMounted(() => {
  // Preload demo data so the dashboard is beautifully populated on first load!
  // The user can still delete/update/register anew.
  businessStore.loadDemoData();
  financialStore.loadDemoData();
});

function handleLogout() {
  authStore.setUser(null);
  router.push('/login');
}

// Live metrics derived from stores
const mapNodesCount = computed(() => {
  if (!businessStore.activeBusiness) return 0;
  return businessStore.competitors.length + 1; // business + competitors
});

const cashAccountsCount = computed(() => {
  return financialStore.reports.length;
});

const systemStatus = computed(() => {
  return businessStore.loading || financialStore.isUploading ? 'Syncing' : 'Online';
});
</script>

<template>
  <div class="min-h-screen bg-slate-50 text-slate-800 font-sans selection:bg-emerald-100 overflow-x-hidden relative flex">
    
    <!-- Blueprint Dotted backdrop overlay -->
    <div class="absolute inset-0 bg-dotted-pattern pointer-events-none opacity-[0.22] z-0"></div>

    <!-- LARGE DESKTOP SIDEBAR -->
    <aside class="hidden lg:flex w-72 h-screen fixed top-0 left-0 bg-white border-r border-slate-200/50 flex-col justify-between z-20 shrink-0 shadow-sm font-sans select-none">
      
      <!-- Top Brand area -->
      <div class="flex-1 overflow-y-auto">
        <div class="p-6 border-b border-slate-100 flex items-center gap-3">
          <VantageLogo class-name="w-10 h-10 hover:scale-105 transition-transform duration-300" />
          <div>
            <h1 class="text-lg font-black tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-emerald-600 to-teal-700 uppercase">
              Vantage AI
            </h1>
            <p class="text-[9px] font-bold text-slate-400 tracking-widest uppercase">Growth Center v1.2</p>
          </div>
        </div>

        <!-- Active Workspace Indicator -->
        <div class="px-6 py-4 border-b border-slate-100/60 bg-slate-50/50">
          <div class="flex items-center justify-between text-[10px] font-black text-slate-450 uppercase tracking-widest mb-1.5">
            <span>Workspace</span>
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
          </div>
          <div class="flex items-center gap-2">
            <div class="w-8 h-8 rounded-lg bg-emerald-600 text-white flex items-center justify-center text-xs font-black">
              {{ businessStore.activeBusiness ? businessStore.activeBusiness.name[0] : 'V' }}
            </div>
            <div class="truncate max-w-[170px]">
              <p class="text-xs font-extrabold text-slate-800 truncate">
                {{ businessStore.activeBusiness ? businessStore.activeBusiness.name : 'Belum Terdaftar' }}
              </p>
              <p class="text-[9px] text-slate-400 font-bold truncate mt-0.5">
                {{ businessStore.activeBusiness ? businessStore.activeBusiness.industry : 'Daftarkan bisnis Anda' }}
              </p>
            </div>
          </div>
        </div>

        <!-- Navigation Menu -->
        <nav class="p-4 space-y-1.5">
          <button 
            @click="activeTab = 'business'"
            :class="[
              'w-full flex items-center justify-between px-4 py-3 rounded-2xl text-xs font-black transition-all duration-200 group',
              activeTab === 'business' 
                ? 'bg-emerald-50 text-emerald-700 shadow-sm border border-emerald-100/50' 
                : 'text-slate-650 hover:bg-slate-50 hover:text-slate-900 border border-transparent'
            ]"
          >
            <span class="flex items-center gap-3">
              <Building :class="['w-5 h-5 transition-transform duration-300 group-hover:scale-105', activeTab === 'business' ? 'text-emerald-600' : 'text-slate-400']" />
              Bisnis
            </span>
            <span v-if="businessStore.activeBusiness" class="w-2 h-2 rounded-full bg-emerald-500"></span>
          </button>

          <button 
            @click="activeTab = 'financial'"
            :class="[
              'w-full flex items-center justify-between px-4 py-3 rounded-2xl text-xs font-black transition-all duration-200 group',
              activeTab === 'financial' 
                ? 'bg-emerald-50 text-emerald-700 shadow-sm border border-emerald-100/50' 
                : 'text-slate-650 hover:bg-slate-50 hover:text-slate-900 border border-transparent'
            ]"
          >
            <span class="flex items-center gap-3">
              <Landmark :class="['w-5 h-5 transition-transform duration-300 group-hover:scale-105', activeTab === 'financial' ? 'text-emerald-600' : 'text-slate-400']" />
              Keuangan
            </span>
            <span v-if="cashAccountsCount > 0" class="badge badge-emerald bg-emerald-100/70 border-none text-[9px] font-black text-emerald-700 px-1.5 py-0.5">
              {{ cashAccountsCount }} PDF
            </span>
          </button>

          <button 
            @click="activeTab = 'profile'"
            :class="[
              'w-full flex items-center justify-between px-4 py-3 rounded-2xl text-xs font-black transition-all duration-200 group',
              activeTab === 'profile' 
                ? 'bg-emerald-50 text-emerald-700 shadow-sm border border-emerald-100/50' 
                : 'text-slate-650 hover:bg-slate-50 hover:text-slate-900 border border-transparent'
            ]"
          >
            <span class="flex items-center gap-3">
              <User :class="['w-5 h-5 transition-transform duration-300 group-hover:scale-105', activeTab === 'profile' ? 'text-emerald-600' : 'text-slate-400']" />
              Profil Akun
            </span>
          </button>
        </nav>

        <!-- Live HUD metrics tracker (makes sidebar feel rich and not empty!) -->
        <div class="mx-4 my-3 bg-slate-50/75 border border-slate-150/60 rounded-2xl p-4.5 space-y-3">
          <span class="text-[9px] font-black text-slate-450 uppercase tracking-widest block select-none">MONITORING SISTEM (READ-ONLY)</span>
          <div class="space-y-2.5">
            <div class="flex items-center justify-between text-[11px] font-semibold text-slate-500">
              <span class="flex items-center gap-1.5"><Compass class="w-4 h-4 text-slate-400" /> Map Nodes</span>
              <span class="font-mono text-slate-700 font-extrabold">{{ mapNodesCount }}</span>
            </div>
            <div class="flex items-center justify-between text-[11px] font-semibold text-slate-500">
              <span class="flex items-center gap-1.5"><FileText class="w-4 h-4 text-slate-400" /> Cash Accounts</span>
              <span class="font-mono text-slate-700 font-extrabold">{{ cashAccountsCount }}</span>
            </div>
            <div class="flex items-center justify-between text-[11px] font-semibold text-slate-500">
              <span class="flex items-center gap-1.5"><Activity class="w-4 h-4 text-slate-400" /> API Gateway</span>
              <span class="font-mono font-black text-emerald-600 flex items-center gap-1 text-[10.5px]">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 inline-block animate-pulse"></span>
                {{ systemStatus }}
              </span>
            </div>
          </div>
        </div>

        <!-- Resources guides list (fills sidebar elegantly) -->
        <div class="px-6 py-4 border-t border-slate-100 space-y-2">
          <span class="text-[9px] font-black text-slate-400 uppercase tracking-widest block">Panduan Pengembang</span>
          <a href="#" class="text-xs font-bold text-slate-500 hover:text-emerald-700 flex items-center justify-between group">
            <span>Market Analysis Guide</span>
            <ChevronRight class="w-3.5 h-3.5 opacity-0 group-hover:opacity-100 transition-opacity" />
          </a>
          <a href="#" class="text-xs font-bold text-slate-500 hover:text-emerald-700 flex items-center justify-between group">
            <span>Developer API Docs</span>
            <ChevronRight class="w-3.5 h-3.5 opacity-0 group-hover:opacity-100 transition-opacity" />
          </a>
          <a href="#" class="text-xs font-bold text-slate-500 hover:text-emerald-700 flex items-center justify-between group">
            <span>Vantage AI Handbook</span>
            <ChevronRight class="w-3.5 h-3.5 opacity-0 group-hover:opacity-100 transition-opacity" />
          </a>
        </div>
      </div>

      <!-- Unified profile card footer -->
      <div class="px-6 py-5 border-t border-slate-150 bg-slate-50/50 shrink-0">
        <div class="flex items-center justify-between gap-2.5">
          <div class="flex items-center gap-2.5">
            <div class="w-9 h-9 rounded-full ring ring-emerald-100 ring-offset-1 overflow-hidden shrink-0">
              <img :src="authStore.user?.photo_url || 'https://api.dicebear.com/7.x/avataaars/svg?seed=' + authStore.user?.email" />
            </div>
            <div class="truncate max-w-[130px] font-sans">
              <p class="text-xs font-extrabold text-slate-800 truncate">{{ authStore.user?.display_name || 'Business Leader' }}</p>
              <p class="text-[9px] text-slate-450 font-mono truncate">{{ authStore.user?.email }}</p>
            </div>
          </div>
          <button @click="handleLogout" class="btn btn-ghost btn-circle btn-sm text-slate-400 hover:text-rose-600 hover:bg-rose-50" title="Keluar">
            <LogOut class="w-4 h-4" />
          </button>
        </div>
      </div>
      
    </aside>

    <!-- MOBILE NAVIGATION HEADER BAR -->
    <div class="lg:hidden w-full bg-white border-b border-slate-200/50 h-16 px-6 flex items-center justify-between absolute top-0 left-0 z-30 select-none shadow-sm">
      <div class="flex items-center gap-2.5">
        <VantageLogo class-name="w-8 h-8" />
        <span class="text-md font-black tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-emerald-600 to-teal-700 uppercase">Vantage AI</span>
      </div>
      
      <button @click="isMobileSidebarOpen = true" class="btn btn-ghost btn-square btn-sm border border-slate-200 rounded-xl">
        <Menu class="w-5 h-5 text-slate-600" />
      </button>
    </div>

    <!-- MOBILE DRAWER / SLIDEOUT MENU OVERLAY -->
    <div v-if="isMobileSidebarOpen" class="lg:hidden fixed inset-0 z-50 flex">
      <!-- Backdrop -->
      <div @click="isMobileSidebarOpen = false" class="absolute inset-0 bg-slate-900/60 backdrop-blur-xs"></div>
      
      <!-- Sidebar Drawer container -->
      <div class="w-72 bg-white h-full relative z-10 flex flex-col justify-between animate-slide-right select-none shadow-2xl">
        <div>
          <!-- Mobile Brand area -->
          <div class="p-6 border-b border-slate-100 flex items-center justify-between">
            <div class="flex items-center gap-3">
              <VantageLogo class-name="w-9 h-9" />
              <div>
                <h1 class="text-md font-black tracking-tight text-emerald-600 uppercase">Vantage AI</h1>
                <p class="text-[9px] font-bold text-slate-400 uppercase tracking-widest">Growth Center</p>
              </div>
            </div>
            <button @click="isMobileSidebarOpen = false" class="btn btn-ghost btn-circle btn-sm">
              <X class="w-5 h-5 text-slate-500" />
            </button>
          </div>

          <!-- Mobile Active Workspace -->
          <div class="px-6 py-4 border-b border-slate-100/60 bg-slate-50/50">
            <div class="flex items-center justify-between text-[10px] font-black text-slate-450 uppercase tracking-widest mb-1.5">
              <span>Workspace</span>
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
            </div>
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 rounded-lg bg-emerald-600 text-white flex items-center justify-center text-xs font-black">
                {{ businessStore.activeBusiness ? businessStore.activeBusiness.name[0] : 'V' }}
              </div>
              <div class="truncate max-w-[170px]">
                <p class="text-xs font-extrabold text-slate-800 truncate">
                  {{ businessStore.activeBusiness ? businessStore.activeBusiness.name : 'Belum Terdaftar' }}
                </p>
              </div>
            </div>
          </div>

          <!-- Mobile Nav list -->
          <nav class="p-4 space-y-1.5">
            <button 
              @click="activeTab = 'business'; isMobileSidebarOpen = false;"
              :class="[
                'w-full flex items-center gap-3 px-4 py-3 rounded-2xl text-xs font-black transition-all',
                activeTab === 'business' ? 'bg-emerald-50 text-emerald-700 shadow-sm' : 'text-slate-650 hover:bg-slate-50'
              ]"
            >
              <Building class="w-5 h-5" />
              Bisnis
            </button>

            <button 
              @click="activeTab = 'financial'; isMobileSidebarOpen = false;"
              :class="[
                'w-full flex items-center gap-3 px-4 py-3 rounded-2xl text-xs font-black transition-all',
                activeTab === 'financial' ? 'bg-emerald-50 text-emerald-700 shadow-sm' : 'text-slate-650 hover:bg-slate-50'
              ]"
            >
              <Landmark class="w-5 h-5" />
              Keuangan
            </button>

            <button 
              @click="activeTab = 'profile'; isMobileSidebarOpen = false;"
              :class="[
                'w-full flex items-center gap-3 px-4 py-3 rounded-2xl text-xs font-black transition-all',
                activeTab === 'profile' ? 'bg-emerald-50 text-emerald-700 shadow-sm' : 'text-slate-650 hover:bg-slate-50'
              ]"
            >
              <User class="w-5 h-5" />
              Profil Akun
            </button>
          </nav>

          <!-- Mobile Guides -->
          <div class="px-6 py-4 border-t border-slate-100 space-y-2">
            <span class="text-[9px] font-black text-slate-400 uppercase tracking-widest block">Panduan</span>
            <a href="#" class="text-xs font-bold text-slate-500 flex items-center justify-between">Market Analysis Guide</a>
            <a href="#" class="text-xs font-bold text-slate-500 flex items-center justify-between">Developer API Docs</a>
          </div>
        </div>

        <!-- Mobile unified profile card footer -->
        <div class="p-4 border-t border-slate-150 bg-slate-50/50 flex items-center justify-between gap-2.5">
          <div class="flex items-center gap-2.5">
            <div class="w-9 h-9 rounded-full ring ring-emerald-100 overflow-hidden shrink-0">
              <img :src="authStore.user?.photo_url || 'https://api.dicebear.com/7.x/avataaars/svg?seed=' + authStore.user?.email" />
            </div>
            <div class="truncate max-w-[130px]">
              <p class="text-xs font-extrabold text-slate-800 truncate">{{ authStore.user?.display_name || 'Business Leader' }}</p>
            </div>
          </div>
          <button @click="handleLogout; isMobileSidebarOpen = false;" class="btn btn-ghost btn-circle btn-sm text-slate-400 hover:text-rose-600">
            <LogOut class="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>

    <!-- MAIN DASHBOARD CONTENT AREA -->
    <main class="flex-1 min-h-screen p-6 md:p-8 lg:p-10 pt-20 lg:pt-10 relative z-10 w-full lg:ml-72">
      
      <!-- Top banner headers dynamically matching active tab -->
      <header class="mb-8 select-none">
        <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-emerald-50 border border-emerald-100/50 text-emerald-700 text-[10px] font-black uppercase tracking-wider shadow-sm mb-3">
          <Sparkles class="w-4 h-4 text-emerald-500 animate-pulse" />
          Growth Suite Active
        </div>
        
        <h2 class="text-3xl md:text-4xl font-black tracking-tight text-slate-900">
          <span v-if="activeTab === 'business'">Market Intelligence Radar</span>
          <span v-else-if="activeTab === 'financial'">Analisis Neraca & Likuiditas</span>
          <span v-else>Konfigurasi Keanggotaan</span>
        </h2>
        
        <p class="text-xs md:text-sm text-slate-500 font-semibold mt-1">
          <span v-if="activeTab === 'business'">Petakan ekosistem pasar kompetitor terdekat, identifikasi ancaman pasar, dan SWOT AI secara real-time.</span>
          <span v-else-if="activeTab === 'financial'">Deteksi kesehatan likuiditas, pola perputaran modal kerja, dan audit kelayakan pinjaman otomatis.</span>
          <span v-else>Perbarui detail data personal, amankan kredensial akun, atau bersihkan basis data riwayat Anda.</span>
        </p>
      </header>

      <!-- Smooth transitions for tab views -->
      <section class="transition-opacity duration-300">
        <BusinessTab v-if="activeTab === 'business'" />
        <FinancialTab v-else-if="activeTab === 'financial'" />
        <ProfileTab v-else />
      </section>

    </main>

  </div>
</template>

<style>
/* Blueprint Dotted Layout background */
.bg-dotted-pattern {
  background-image: radial-gradient(#cbd5e1 1.2px, transparent 1.2px);
  background-size: 24px 24px;
}

@keyframes slide-right {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(0); }
}

.animate-slide-right {
  animation: slide-right 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
</style>
