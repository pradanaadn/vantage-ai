<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { signInWithEmailAndPassword } from 'firebase/auth';
import { auth } from '../../firebase';
import { authService } from '../../services/auth.service';
import { useAuthStore } from '../../stores/auth';
import { ShieldCheck, Radar, Telescope, ArrowRight, Sparkles, Eye, EyeOff, CheckCircle2, AlertCircle } from 'lucide-vue-next';
import copy from '../../assets/copy.json';
import VantageLogo from '../../components/base/VantageLogo.vue';

const router = useRouter();
const authStore = useAuthStore();
const authCopy = copy.auth.login;
const branding = copy.auth.branding;

const email = ref('');
const password = ref('');
const loading = ref(false);
const error = ref('');
const successAlert = ref('');

// Password visibility toggle
const showPassword = ref(false);
function togglePasswordVisibility() {
  showPassword.value = !showPassword.value;
}

// Input touched/dirty states
const emailTouched = ref(false);
const passwordTouched = ref(false);

const iconMap: Record<string, any> = {
  ShieldCheck,
  Radar,
  Telescope
};

// Email validation matching backend standard format
const isEmailValid = computed(() => {
  const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return re.test(email.value);
});

const emailError = computed(() => {
  if (!emailTouched.value || !email.value) return '';
  if (!isEmailValid.value) return 'Please enter a valid email address.';
  return '';
});

// Password validation matching backend requirements
const isPasswordValid = computed(() => {
  return password.value.length >= 8;
});

const passwordError = computed(() => {
  if (!passwordTouched.value || !password.value) return '';
  if (!isPasswordValid.value) return 'Password must be at least 8 characters.';
  return '';
});

// Overall Form Validity
const isFormValid = computed(() => {
  return isEmailValid.value && isPasswordValid.value;
});

async function handleLogin() {
  if (!isFormValid.value) {
    error.value = 'Please correct the errors before signing in.';
    return;
  }

  loading.value = true;
  error.value = '';
  successAlert.value = '';
  
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email.value, password.value);
    const idToken = await userCredential.user.getIdToken();
    const userData = await authService.login(idToken);
    
    authStore.setUser({
      uid: userData.uid,
      email: userData.email,
      display_name: userData.display_name,
      photo_url: userData.photo_url
    });
    
    // Display successful login alert
    successAlert.value = `Welcome back, ${userData.display_name || 'Business Leader'}! Opening your Growth Center...`;
    
    setTimeout(() => {
      router.push('/dashboard');
    }, 1200);
  } catch (err: any) {
    console.error(err);
    error.value = 'Authentication failed. Please verify your credentials.';
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="min-h-screen flex flex-col md:flex-row bg-slate-50 text-slate-800 font-sans selection:bg-emerald-100 overflow-x-hidden">
    
    <!-- Custom CSS Dotted Grid Backdrop overlay in Left Panel -->
    <div class="absolute inset-0 bg-dotted-pattern pointer-events-none opacity-[0.25] z-0"></div>

    <!-- Left Panel: Friendly Growth Onboarding -->
    <div class="md:w-3/5 bg-gradient-to-br from-slate-100 to-emerald-50/40 p-8 md:p-20 flex flex-col justify-center relative overflow-hidden border-r border-slate-200/50">
      
      <!-- Organic Green Gradient Blurs -->
      <div class="absolute inset-0 opacity-40 pointer-events-none z-0">
        <div class="absolute top-10 left-10 w-[450px] h-[450px] bg-gradient-to-br from-emerald-200 to-teal-100 blur-[130px] rounded-full"></div>
        <div class="absolute bottom-10 right-10 w-[500px] h-[500px] bg-amber-100 blur-[140px] rounded-full"></div>
      </div>
      
      <div class="relative z-10 max-w-xl space-y-8">
        <div class="flex flex-col gap-4">
          <VantageLogo class-name="w-20 h-20 hover:scale-105 transition-transform duration-300 drop-shadow-sm" />
          <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-50 border border-emerald-200/60 text-emerald-700 text-xs font-black uppercase tracking-wider shadow-sm w-fit">
            <Sparkles class="w-3.5 h-3.5 text-emerald-500 animate-pulse" />
            Unlock Business Insights
          </div>
        </div>

        <div class="space-y-3">
          <h1 class="text-5xl md:text-6xl font-black tracking-tighter text-slate-900 leading-none">
            {{ branding.name }}
          </h1>
          <p class="text-lg text-slate-600 font-semibold leading-relaxed max-w-md">
            {{ branding.slogan }}
          </p>
        </div>
        
        <!-- Overlapping custom grid panels to break standard AI look -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 pt-4">
          <div v-for="pillar in branding.pillars" :key="pillar.id" class="group bg-white/80 backdrop-blur-md p-5 rounded-2xl border border-slate-200/60 shadow-sm hover:shadow-md hover:border-emerald-300 transition-all duration-300 border-l-4 border-l-emerald-500">
            <div class="flex items-center gap-3.5 mb-2">
              <div class="bg-emerald-50 p-2.5 rounded-xl border border-emerald-100 text-emerald-600 group-hover:scale-105 transition-transform shrink-0">
                <component :is="iconMap[pillar.icon] || ShieldCheck" class="w-5 h-5" />
              </div>
              <h3 class="text-base font-bold text-slate-900">{{ pillar.title }}</h3>
            </div>
            <p class="text-slate-500 text-xs leading-relaxed font-semibold">
              {{ pillar.description }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Panel: Access Portal -->
    <div class="md:w-2/5 flex items-center justify-center p-8 bg-white relative z-10">
      <div class="w-full max-w-md">
        <div class="mb-10 text-center md:text-left">
          <h2 class="text-4xl font-black text-slate-900 mb-2 tracking-tight">{{ authCopy.title }}</h2>
          <p class="text-slate-400 font-bold text-sm">{{ authCopy.subtitle }}</p>
        </div>
        
        <!-- Alert banners -->
        <transition name="fade">
          <div v-if="successAlert" class="alert bg-emerald-50 border border-emerald-200 text-emerald-800 text-sm rounded-xl mb-6 p-4 flex gap-3 shadow-sm">
            <CheckCircle2 class="w-5 h-5 shrink-0 text-emerald-600 animate-bounce" />
            <span class="font-bold">{{ successAlert }}</span>
          </div>
        </transition>

        <transition name="fade">
          <div v-if="error" class="alert bg-rose-50 border border-rose-100 text-rose-700 text-sm rounded-xl mb-6 p-4 flex gap-3 shadow-sm">
            <ShieldCheck class="w-5 h-5 shrink-0 text-rose-500 animate-pulse" />
            <span class="font-semibold">{{ error }}</span>
          </div>
        </transition>

        <form @submit.prevent="handleLogin" class="space-y-6">
          
          <!-- Email Input with error message inside label row -->
          <div class="space-y-2">
            <div class="flex justify-between items-center ml-1">
              <label class="text-xs font-black text-slate-400 uppercase tracking-widest">
                {{ authCopy.emailLabel }}
              </label>
              <span v-if="emailError" class="text-[11px] text-rose-500 font-extrabold flex items-center gap-1">
                <AlertCircle class="w-3.5 h-3.5" />
                {{ emailError }}
              </span>
            </div>
            <input 
              v-model="email" 
              @blur="emailTouched = true"
              @input="emailTouched = true"
              type="email" 
              placeholder="name@company.com" 
              class="w-full bg-white border rounded-xl px-5 py-4 text-slate-800 focus:bg-emerald-50/10 focus:outline-none focus:ring-4 transition-all placeholder:text-slate-400 font-semibold" 
              :class="[emailError ? 'border-rose-300 focus:ring-rose-500/10 focus:border-rose-500' : 'border-slate-200/80 focus:ring-emerald-500/10 focus:border-emerald-500']"
              required 
            />
          </div>
          
          <!-- Password Input with hide/show toggle and error message -->
          <div class="space-y-2">
            <div class="flex justify-between items-center ml-1">
              <label class="text-xs font-black text-slate-400 uppercase tracking-widest">
                {{ authCopy.passwordLabel }}
              </label>
              <span v-if="passwordError" class="text-[11px] text-rose-500 font-extrabold flex items-center gap-1">
                <AlertCircle class="w-3.5 h-3.5" />
                {{ passwordError }}
              </span>
            </div>
            <div class="relative">
              <input 
                v-model="password" 
                @blur="passwordTouched = true"
                @input="passwordTouched = true"
                :type="showPassword ? 'text' : 'password'" 
                placeholder="••••••••" 
                class="w-full bg-white border rounded-xl pl-5 pr-12 py-4 text-slate-800 focus:bg-emerald-50/10 focus:outline-none focus:ring-4 transition-all placeholder:text-slate-400 font-semibold" 
                :class="[passwordError ? 'border-rose-300 focus:ring-rose-500/10 focus:border-rose-500' : 'border-slate-200/80 focus:ring-emerald-500/10 focus:border-emerald-500']"
                required 
              />
              <button 
                type="button" 
                @click="togglePasswordVisibility"
                class="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors p-1 rounded-md"
              >
                <component :is="showPassword ? EyeOff : Eye" class="w-5 h-5" />
              </button>
            </div>
          </div>

          <div class="flex justify-end pt-1">
            <a href="#" class="text-xs font-bold text-emerald-600 hover:text-emerald-700 transition-colors">
              {{ authCopy.forgotPassword }}
            </a>
          </div>
          
          <button 
            type="submit" 
            class="group relative w-full bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white font-bold py-4 rounded-xl shadow-lg shadow-emerald-500/20 transition-all flex items-center justify-center gap-3 active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed" 
            :disabled="loading || !isFormValid"
          >
            <span v-if="loading" class="loading loading-spinner w-5 text-white"></span>
            <template v-else>
              {{ authCopy.submitButton }}
              <ArrowRight class="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </template>
          </button>
        </form>
        
        <div class="relative my-10">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-slate-200/60"></div>
          </div>
          <div class="relative flex justify-center text-xs uppercase tracking-widest text-slate-400 bg-white px-4 font-black">
            {{ authCopy.dividerText }}
          </div>
        </div>
        
        <div class="text-center">
          <p class="text-slate-500 text-sm font-semibold">
            {{ authCopy.footerText }} 
            <router-link to="/signup" class="text-emerald-600 hover:text-emerald-700 font-black ml-1 transition-colors border-b border-emerald-200 hover:border-emerald-500">
              {{ authCopy.footerLink }}
            </router-link>
          </p>
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
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
