<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { authService } from '../../services/auth.service';
import { ShieldCheck, CheckCircle2, UserPlus, ArrowRight, Sparkles, Eye, EyeOff, AlertCircle } from 'lucide-vue-next';
import copy from '../../assets/copy.json';
import VantageLogo from '../../components/base/VantageLogo.vue';

const router = useRouter();
const authCopy = copy.auth.signup;
const branding = copy.auth.branding;

const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const displayName = ref('');
const loading = ref(false);
const error = ref('');
const successAlert = ref('');

// Input touched/dirty states
const nameTouched = ref(false);
const emailTouched = ref(false);
const passwordTouched = ref(false);
const confirmTouched = ref(false);

// Password visibility toggles
const showPassword = ref(false);
const showConfirmPassword = ref(false);

function togglePasswordVisibility() {
  showPassword.value = !showPassword.value;
}
function toggleConfirmVisibility() {
  showConfirmPassword.value = !showConfirmPassword.value;
}

// Input checkers
const isNameValid = computed(() => {
  return displayName.value.trim().length > 0;
});

const isEmailValid = computed(() => {
  const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return re.test(email.value);
});

// Password checklist components matching the backend (auth.py)
const hasMinLength = computed(() => password.value.length >= 8);
const hasUppercase = computed(() => /[A-Z]/.test(password.value));
const hasLowercase = computed(() => /[a-z]/.test(password.value));
const hasDigit = computed(() => /\d/.test(password.value));

const isPasswordValid = computed(() => {
  return hasMinLength.value && hasUppercase.value && hasLowercase.value && hasDigit.value;
});

const isConfirmValid = computed(() => {
  return password.value === confirmPassword.value;
});

// Inline error calculations
const nameError = computed(() => {
  if (!nameTouched.value || !displayName.value) return '';
  if (!isNameValid.value) return 'Full Name is required.';
  return '';
});

const emailError = computed(() => {
  if (!emailTouched.value || !email.value) return '';
  if (!isEmailValid.value) return 'Please enter a valid email address.';
  return '';
});

const passwordError = computed(() => {
  if (!passwordTouched.value || !password.value) return '';
  if (!isPasswordValid.value) return 'Password does not meet all criteria.';
  return '';
});

const confirmError = computed(() => {
  if (!confirmTouched.value || !confirmPassword.value) return '';
  if (!isConfirmValid.value) return 'Passwords do not match.';
  return '';
});

// Overall Form Validity
const isFormValid = computed(() => {
  return isNameValid.value && isEmailValid.value && isPasswordValid.value && isConfirmValid.value;
});

async function handleSignup() {
  if (!isFormValid.value) {
    error.value = "Please complete all fields correctly.";
    return;
  }

  loading.value = true;
  error.value = '';
  successAlert.value = '';
  
  try {
    await authService.signup(email.value, password.value, displayName.value);
    
    // Display successful signup alert
    successAlert.value = "Account created successfully! Redirecting to Sign In...";
    
    setTimeout(() => {
      router.push('/login');
    }, 1500);
  } catch (err: any) {
    console.error(err);
    error.value = err.response?.data?.detail || err.message || 'Signup failed. Please verify your details.';
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
        <div class="absolute top-20 left-1/4 w-[400px] h-[400px] bg-gradient-to-br from-emerald-200 to-teal-100 blur-[130px] rounded-full"></div>
        <div class="absolute bottom-20 right-1/4 w-[500px] h-[500px] bg-amber-100 blur-[140px] rounded-full"></div>
      </div>
      
      <div class="relative z-10 max-w-lg space-y-8">
        <div class="flex flex-col gap-4">
          <VantageLogo class-name="w-20 h-20 hover:scale-105 transition-transform duration-300 drop-shadow-sm" />
          <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-50 border border-emerald-100 text-emerald-700 text-xs font-black uppercase tracking-wider shadow-sm w-fit">
            <UserPlus class="w-3.5 h-3.5 text-emerald-500" />
            Join Vantage AI
          </div>
        </div>

        <div class="space-y-3">
          <h1 class="text-5xl md:text-6xl font-black tracking-tighter text-slate-900 uppercase leading-none">
            {{ authCopy.title }}
          </h1>
          <p class="text-lg text-slate-600 font-semibold leading-relaxed">
            {{ authCopy.subtitle }}
          </p>
        </div>
        
        <!-- Checklist card with premium offset layout -->
        <div class="space-y-6 bg-white/85 backdrop-blur-xl p-8 rounded-3xl border border-slate-200/50 shadow-md relative overflow-hidden border-l-4 border-l-emerald-500">
          <h3 class="text-base font-black text-slate-900 uppercase tracking-wider flex items-center gap-2">
            <Sparkles class="w-4.5 h-4.5 text-amber-500 animate-pulse" />
            {{ branding.signupHighlights.title }}
          </h3>
          <ul class="space-y-5">
            <li v-for="(item, index) in branding.signupHighlights.items" :key="index" 
                class="flex items-start gap-4 group transition-all duration-300">
              <div class="bg-emerald-50 p-1.5 rounded-lg border border-emerald-100 group-hover:bg-emerald-100 transition-colors shrink-0">
                <CheckCircle2 class="w-5 h-5 text-emerald-600" />
              </div>
              <span class="text-slate-700 font-semibold leading-snug group-hover:text-slate-900 transition-colors">
                {{ item }}
              </span>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Right Panel: Signup Form -->
    <div class="md:w-2/5 flex items-center justify-center p-8 bg-white relative z-10">
      <div class="w-full max-w-md">
        <div class="mb-10 text-center md:text-left">
          <h2 class="text-4xl font-black text-slate-900 mb-2 tracking-tight">Create Account</h2>
          <p class="text-slate-450 font-bold text-sm">Join hundreds of growing SMB businesses</p>
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

        <form @submit.prevent="handleSignup" class="space-y-4">
          
          <!-- Full Name -->
          <div class="space-y-1">
            <div class="flex justify-between items-center ml-1">
              <label class="text-xs font-black text-slate-400 uppercase tracking-widest">
                {{ authCopy.nameLabel }}
              </label>
              <span v-if="nameError" class="text-[10px] text-rose-500 font-extrabold flex items-center gap-1">
                <AlertCircle class="w-3 h-3" />
                {{ nameError }}
              </span>
            </div>
            <input 
              v-model="displayName" 
              @blur="nameTouched = true"
              @input="nameTouched = true"
              type="text" 
              placeholder="Full Name" 
              class="w-full bg-white border rounded-xl px-5 py-3 text-slate-800 focus:bg-emerald-50/10 focus:outline-none focus:ring-4 transition-all placeholder:text-slate-400 font-semibold" 
              :class="[nameError ? 'border-rose-300 focus:ring-rose-500/10 focus:border-rose-500' : 'border-slate-200/80 focus:ring-emerald-500/10 focus:border-emerald-500']"
              required
            />
          </div>

          <!-- Business Email -->
          <div class="space-y-1">
            <div class="flex justify-between items-center ml-1">
              <label class="text-xs font-black text-slate-400 uppercase tracking-widest">
                {{ authCopy.emailLabel }}
              </label>
              <span v-if="emailError" class="text-[10px] text-rose-500 font-extrabold flex items-center gap-1">
                <AlertCircle class="w-3 h-3" />
                {{ emailError }}
              </span>
            </div>
            <input 
              v-model="email" 
              @blur="emailTouched = true"
              @input="emailTouched = true"
              type="email" 
              placeholder="name@company.com" 
              class="w-full bg-white border rounded-xl px-5 py-3 text-slate-800 focus:bg-emerald-50/10 focus:outline-none focus:ring-4 transition-all placeholder:text-slate-400 font-semibold" 
              :class="[emailError ? 'border-rose-300 focus:ring-rose-500/10 focus:border-rose-500' : 'border-slate-200/80 focus:ring-emerald-500/10 focus:border-emerald-500']"
              required 
            />
          </div>
          
          <!-- Password and Confirm Password Row -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            
            <!-- Password input with eye toggle -->
            <div class="space-y-1">
              <div class="flex justify-between items-center ml-1">
                <label class="text-xs font-black text-slate-400 uppercase tracking-widest">
                  Password
                </label>
                <span v-if="passwordError" class="text-[10px] text-rose-500 font-extrabold flex items-center gap-1">
                  <AlertCircle class="w-3 h-3" />
                  Criteria Error
                </span>
              </div>
              <div class="relative">
                <input 
                  v-model="password" 
                  @blur="passwordTouched = true"
                  @input="passwordTouched = true"
                  :type="showPassword ? 'text' : 'password'" 
                  placeholder="••••••••" 
                  class="w-full bg-white border rounded-xl pl-5 pr-10 py-3 text-slate-800 focus:bg-emerald-50/10 focus:outline-none focus:ring-4 transition-all placeholder:text-slate-400 font-semibold" 
                  :class="[passwordError ? 'border-rose-300 focus:ring-rose-500/10 focus:border-rose-500' : 'border-slate-200/80 focus:ring-emerald-500/10 focus:border-emerald-500']"
                  required 
                />
                <button 
                  type="button" 
                  @click="togglePasswordVisibility"
                  class="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors p-0.5 rounded"
                >
                  <component :is="showPassword ? EyeOff : Eye" class="w-4.5 h-4.5" />
                </button>
              </div>
            </div>

            <!-- Confirm Password input with eye toggle -->
            <div class="space-y-1">
              <div class="flex justify-between items-center ml-1">
                <label class="text-xs font-black text-slate-400 uppercase tracking-widest">
                  Confirm
                </label>
                <span v-if="confirmError" class="text-[10px] text-rose-500 font-extrabold flex items-center gap-1">
                  <AlertCircle class="w-3 h-3" />
                  Mismatch
                </span>
              </div>
              <div class="relative">
                <input 
                  v-model="confirmPassword" 
                  @blur="confirmTouched = true"
                  @input="confirmTouched = true"
                  :type="showConfirmPassword ? 'text' : 'password'" 
                  placeholder="••••••••" 
                  class="w-full bg-white border rounded-xl pl-5 pr-10 py-3 text-slate-800 focus:bg-emerald-50/10 focus:outline-none focus:ring-4 transition-all placeholder:text-slate-400 font-semibold" 
                  :class="[confirmError ? 'border-rose-300 focus:ring-rose-500/10 focus:border-rose-500' : 'border-slate-200/80 focus:ring-emerald-500/10 focus:border-emerald-500']"
                  required 
                />
                <button 
                  type="button" 
                  @click="toggleConfirmVisibility"
                  class="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors p-0.5 rounded"
                >
                  <component :is="showConfirmPassword ? EyeOff : Eye" class="w-4.5 h-4.5" />
                </button>
              </div>
            </div>

          </div>

          <!-- Password requirements checklist -->
          <div class="bg-slate-50 p-4 rounded-xl border border-slate-200/50 space-y-2.5 text-xs text-slate-500 font-semibold mt-2">
            <p class="font-black text-[10px] text-slate-400 uppercase tracking-widest border-b border-slate-200 pb-1.5">Password Criteria:</p>
            <div class="grid grid-cols-2 gap-2">
              <span class="flex items-center gap-1.5" :class="[hasMinLength ? 'text-emerald-600' : 'text-slate-450']">
                <CheckCircle2 class="w-4 h-4" :class="[hasMinLength ? 'text-emerald-500' : 'text-slate-300']" />
                8+ Characters
              </span>
              <span class="flex items-center gap-1.5" :class="[hasUppercase ? 'text-emerald-600' : 'text-slate-450']">
                <CheckCircle2 class="w-4 h-4" :class="[hasUppercase ? 'text-emerald-500' : 'text-slate-300']" />
                1 Uppercase (A-Z)
              </span>
              <span class="flex items-center gap-1.5" :class="[hasLowercase ? 'text-emerald-600' : 'text-slate-450']">
                <CheckCircle2 class="w-4 h-4" :class="[hasLowercase ? 'text-emerald-500' : 'text-slate-300']" />
                1 Lowercase (a-z)
              </span>
              <span class="flex items-center gap-1.5" :class="[hasDigit ? 'text-emerald-600' : 'text-slate-450']">
                <CheckCircle2 class="w-4 h-4" :class="[hasDigit ? 'text-emerald-500' : 'text-slate-300']" />
                1 Number (0-9)
              </span>
            </div>
          </div>
          
          <button 
            type="submit" 
            class="group relative w-full bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white font-bold py-4 rounded-xl shadow-lg shadow-emerald-500/20 transition-all flex items-center justify-center gap-3 active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed mt-4" 
            :disabled="loading || !isFormValid"
          >
            <span v-if="loading" class="loading loading-spinner w-5 text-white"></span>
            <template v-else>
              {{ authCopy.submitButton }}
              <ArrowRight class="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </template>
          </button>
        </form>
        
        <div class="text-center mt-8 pt-4 border-t border-slate-200/60">
          <p class="text-slate-500 text-sm font-semibold">
            {{ authCopy.footerText }} 
            <router-link to="/login" class="text-emerald-600 hover:text-emerald-700 font-extrabold ml-1 transition-colors border-b border-emerald-200 hover:border-emerald-500">
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
