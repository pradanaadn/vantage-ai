<script setup lang="ts">
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';
import { LogOut, User, Settings, Sparkles } from 'lucide-vue-next';
import VantageLogo from '../components/base/VantageLogo.vue';

const authStore = useAuthStore();
const router = useRouter();

function handleLogout() {
  authStore.setUser(null);
  router.push('/login');
}
</script>

<template>
  <div class="min-h-screen bg-slate-50 text-slate-800 font-sans selection:bg-emerald-100 overflow-x-hidden relative">
    
    <!-- Blueprint Dotted backdrop overlay -->
    <div class="absolute inset-0 bg-dotted-pattern pointer-events-none opacity-[0.25] z-0"></div>

    <!-- Navbar -->
    <div class="navbar bg-white border-b border-slate-200/50 px-6 md:px-8 shadow-sm relative z-10">
      <div class="flex-1 flex items-center gap-3">
        <VantageLogo class-name="w-10 h-10 hover:scale-105 transition-transform duration-300" />
        <a class="text-xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-emerald-600 to-teal-700 uppercase select-none">Vantage AI</a>
      </div>
      
      <div class="flex-none gap-4">
        <div class="dropdown dropdown-end">
          <label tabindex="0" class="btn btn-ghost btn-circle avatar border border-emerald-100 hover:border-emerald-400 transition-colors">
            <div class="w-10 rounded-full font-semibold">
              <img :src="authStore.user?.photo_url || 'https://api.dicebear.com/7.x/avataaars/svg?seed=' + authStore.user?.email" />
            </div>
          </label>
          <ul tabindex="0" class="mt-3 p-2 shadow-2xl menu menu-sm dropdown-content bg-white border border-slate-200/60 rounded-2xl w-52 z-50 text-slate-700">
            <li class="px-3.5 py-2 border-b border-slate-100 mb-1">
              <p class="text-xs font-black text-slate-400 uppercase tracking-widest p-0">Signed in as</p>
              <p class="text-sm font-bold text-slate-800 truncate p-0 font-sans">{{ authStore.user?.display_name || 'Business Owner' }}</p>
            </li>
            <li><a class="hover:bg-emerald-50 hover:text-emerald-700 font-bold py-2.5 rounded-xl"><User class="w-4 h-4" /> Profile</a></li>
            <li><a class="hover:bg-emerald-50 hover:text-emerald-700 font-bold py-2.5 rounded-xl"><Settings class="w-4 h-4" /> Settings</a></li>
            <li><a @click="handleLogout" class="hover:bg-rose-50 hover:text-rose-600 font-bold py-2.5 rounded-xl border-t border-slate-100 mt-1"><LogOut class="w-4 h-4" /> Logout</a></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Main Workspace Greeting -->
    <div class="p-6 md:p-12 max-w-5xl mx-auto relative z-10">
      <div class="bg-white rounded-3xl border border-slate-200/60 overflow-hidden relative shadow-lg border-t-8 border-t-emerald-600">
        
        <!-- Glowing Ambient Backdrop inside welcome Card -->
        <div class="absolute inset-0 z-0 opacity-20 pointer-events-none">
          <div class="absolute -top-10 -left-10 w-[300px] h-[300px] bg-emerald-300 blur-[100px] rounded-full"></div>
          <div class="absolute -bottom-10 -right-10 w-[400px] h-[400px] bg-amber-200 blur-[120px] rounded-full"></div>
        </div>

        <div class="p-10 md:p-16 text-center relative z-10">
          <div class="max-w-xl mx-auto space-y-6">
            <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-emerald-50 border border-emerald-100 text-emerald-700 text-xs font-black uppercase tracking-wider shadow-sm">
              <Sparkles class="w-4.5 h-4.5 text-emerald-500 animate-pulse" />
              Growth Suite Online
            </div>
            
            <h1 class="text-4xl md:text-5xl font-black tracking-tight text-slate-900 leading-tight">
              Hello, {{ authStore.user?.display_name || 'Business Leader' }}!
            </h1>
            
            <p class="text-base md:text-lg text-slate-600 font-semibold leading-relaxed">
              Welcome to your Vantage AI Growth Center. Your workspace is fully optimized, secure, and ready to help you analyze margins, map local markets, and build a highly profitable future.
            </p>
            
            <div class="pt-4">
              <button class="bg-gradient-to-r from-emerald-500 to-teal-600 text-white font-bold px-8 py-3.5 rounded-xl hover:from-emerald-600 hover:to-teal-700 transition-all shadow-lg shadow-emerald-500/20 active:scale-95">
                Go to Dashboard
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
/* Blueprint Dotted Layout background */
.bg-dotted-pattern {
  background-image: radial-gradient(#cbd5e1 1.2px, transparent 1.2px);
  background-size: 24px 24px;
}
</style>
