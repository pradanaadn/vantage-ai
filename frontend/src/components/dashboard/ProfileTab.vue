<script setup lang="ts">
import { ref, computed } from 'vue';
import { useAuthStore } from '../../stores/auth';
import { useBusinessStore } from '../../stores/business';
import { useFinancialStore } from '../../stores/financial';
import { useRouter } from 'vue-router';
import { 
  User, Camera, Trash2, AlertTriangle, 
  CheckCircle2, ShieldAlert, RefreshCw 
} from 'lucide-vue-next';

const authStore = useAuthStore();
const businessStore = useBusinessStore();
const financialStore = useFinancialStore();
const router = useRouter();

const displayName = ref(authStore.user?.display_name || '');
const email = ref(authStore.user?.email || '');
const photoUrl = ref(authStore.user?.photo_url || '');
const newPassword = ref('');
const confirmPassword = ref('');

const successMessage = ref('');
const errorMessage = ref('');
const isSaving = ref(false);

// Input touched states for real-time validation triggers
const isDisplayNameTouched = ref(false);
const isEmailTouched = ref(false);
const isNewPasswordTouched = ref(false);
const isConfirmPasswordTouched = ref(false);

// Double confirmation deletion modal state
const showDeleteModal = ref(false);
const confirmDeleteText = ref('');
const deleteError = ref('');

// Auto-generated avatar based on email seed
const avatarUrl = computed(() => {
  if (photoUrl.value) return photoUrl.value;
  return 'https://api.dicebear.com/7.x/avataaars/svg?seed=' + (email.value || 'vantage-user');
});

// Real-time client-side validation logic aligned with Pydantic schemas
const isDisplayNameValid = computed(() => {
  return displayName.value.trim().length > 0;
});

const isEmailValid = computed(() => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email.value.trim());
});

const isNewPasswordValid = computed(() => {
  if (!newPassword.value) return true; // Empty password is valid (indicates no password change)
  return newPassword.value.length >= 8;
});

const isConfirmPasswordValid = computed(() => {
  if (!newPassword.value) return true;
  return confirmPassword.value === newPassword.value;
});

const isFormValid = computed(() => {
  return isDisplayNameValid.value && 
         isEmailValid.value && 
         isNewPasswordValid.value && 
         isConfirmPasswordValid.value;
});

async function handleUpdateProfile() {
  // Trigger validation borders immediately upon submit attempt
  isDisplayNameTouched.value = true;
  isEmailTouched.value = true;
  isNewPasswordTouched.value = true;
  isConfirmPasswordTouched.value = true;

  errorMessage.value = '';
  successMessage.value = '';

  if (!isFormValid.value) {
    errorMessage.value = 'Silakan perbaiki kesalahan pada formulir di bawah.';
    return;
  }

  isSaving.value = true;

  try {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 800));
    
    // Update local store
    authStore.setUser({
      ...authStore.user,
      uid: authStore.user?.uid || 'user_default',
      display_name: displayName.value,
      email: email.value,
      photo_url: photoUrl.value
    });

    successMessage.value = 'Profil Anda berhasil diperbarui!';
    newPassword.value = '';
    confirmPassword.value = '';
    
    // Reset touched states
    isDisplayNameTouched.value = false;
    isEmailTouched.value = false;
    isNewPasswordTouched.value = false;
    isConfirmPasswordTouched.value = false;
  } catch (err: any) {
    errorMessage.value = err.message || 'Gagal memperbarui profil.';
  } finally {
    isSaving.value = false;
  }
}

async function handleDeleteAccount() {
  deleteError.value = '';
  if (confirmDeleteText.value !== 'HAPUS AKUN') {
    deleteError.value = 'Konfirmasi teks salah. Silakan ketik "HAPUS AKUN" dengan tepat.';
    return;
  }

  try {
    // Simulate deletion API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Clean all stores
    businessStore.activeBusiness = null;
    businessStore.competitors = [];
    financialStore.reports = [];
    financialStore.analysis = null;
    authStore.setUser(null);

    showDeleteModal.value = false;
    router.push('/signup');
  } catch (err: any) {
    deleteError.value = err.message || 'Gagal menghapus akun.';
  }
}
</script>

<template>
  <div class="max-w-3xl mx-auto space-y-8 font-sans">
    
    <!-- Profile main details edit -->
    <div class="bg-white rounded-3xl border border-slate-200/60 p-6 md:p-8 shadow-md">
      <div class="border-b border-slate-100 pb-5 mb-6 select-none">
        <h2 class="text-xl font-extrabold text-slate-800 flex items-center gap-2">
          <User class="w-5.5 h-5.5 text-emerald-600" />
          Pengaturan Akun Pengguna
        </h2>
        <p class="text-xs text-slate-500 font-semibold mt-1">Kelola informasi profil, display name, avatar, dan keamanan sandi Anda</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
        
        <!-- Left Side: Avatar Display (4 cols) -->
        <div class="md:col-span-4 flex flex-col items-center gap-4 text-center select-none">
          <div class="relative group/avatar">
            <div class="w-28 h-28 rounded-full ring ring-emerald-100 ring-offset-2 overflow-hidden bg-slate-50 flex items-center justify-center shadow-lg transition-transform duration-300 group-hover/avatar:scale-[1.02]">
              <img :src="avatarUrl" alt="User Avatar" class="w-full h-full object-cover" />
            </div>
            <div class="absolute bottom-1 right-1 w-8 h-8 rounded-full bg-slate-900 text-white flex items-center justify-center border-2 border-white shadow shadow-slate-400">
              <Camera class="w-4 h-4" />
            </div>
          </div>
          <div>
            <h3 class="text-sm font-black text-slate-800 truncate max-w-[200px]">{{ displayName || 'Business Leader' }}</h3>
            <p class="text-[10px] text-slate-400 font-mono mt-0.5 truncate max-w-[200px]">{{ email }}</p>
          </div>
        </div>

        <!-- Right Side: Edit Inputs Form (8 cols) -->
        <form @submit.prevent="handleUpdateProfile" class="md:col-span-8 space-y-5">
          
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="form-control w-full">
              <label class="label"><span class="label-text font-black text-slate-700 text-[10px] uppercase tracking-wider">Nama Lengkap</span></label>
              <input 
                type="text" 
                v-model="displayName"
                @blur="isDisplayNameTouched = true"
                placeholder="Contoh: Budi Santoso"
                :class="[
                  'input input-bordered focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 rounded-xl text-xs font-semibold w-full text-slate-800',
                  { 'border-rose-500 focus:border-rose-500 focus:ring-rose-500': isDisplayNameTouched && !isDisplayNameValid }
                ]" 
              />
              <p v-if="isDisplayNameTouched && !isDisplayNameValid" class="text-[10px] text-rose-500 font-bold mt-1">Nama lengkap tidak boleh kosong.</p>
            </div>

            <div class="form-control w-full">
              <label class="label"><span class="label-text font-black text-slate-700 text-[10px] uppercase tracking-wider">Alamat Email</span></label>
              <input 
                type="email" 
                v-model="email"
                @blur="isEmailTouched = true"
                placeholder="budi@example.com"
                :class="[
                  'input input-bordered focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 rounded-xl text-xs font-semibold w-full text-slate-800',
                  { 'border-rose-500 focus:border-rose-500 focus:ring-rose-500': isEmailTouched && !isEmailValid }
                ]" 
              />
              <p v-if="isEmailTouched && !isEmailValid" class="text-[10px] text-rose-500 font-bold mt-1">Format email tidak valid.</p>
            </div>
          </div>

          <div class="form-control w-full">
            <label class="label">
              <span class="label-text font-black text-slate-700 text-[10px] uppercase tracking-wider">URL Foto Profil / Avatar</span>
            </label>
            <input 
              type="url" 
              v-model="photoUrl"
              placeholder="https://images.unsplash.com/... atau kosongkan untuk auto-generasi" 
              class="input input-bordered focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 rounded-xl text-xs font-medium w-full text-slate-800" 
            />
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 border-t border-slate-100 pt-4">
            <div class="form-control w-full">
              <label class="label"><span class="label-text font-black text-slate-700 text-[10px] uppercase tracking-wider">Kata Sandi Baru</span></label>
              <input 
                type="password" 
                v-model="newPassword"
                @blur="isNewPasswordTouched = true"
                placeholder="Minimal 8 karakter"
                :class="[
                  'input input-bordered focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 rounded-xl text-xs font-semibold w-full text-slate-800',
                  { 'border-rose-500 focus:border-rose-500 focus:ring-rose-500': isNewPasswordTouched && !isNewPasswordValid }
                ]" 
              />
              <p v-if="isNewPasswordTouched && !isNewPasswordValid" class="text-[10px] text-rose-500 font-bold mt-1">Kata sandi baru minimal harus 8 karakter.</p>
            </div>

            <div class="form-control w-full">
              <label class="label"><span class="label-text font-black text-slate-700 text-[10px] uppercase tracking-wider">Konfirmasi Sandi Baru</span></label>
              <input 
                type="password" 
                v-model="confirmPassword"
                @blur="isConfirmPasswordTouched = true"
                placeholder="Ulangi sandi baru"
                :class="[
                  'input input-bordered focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 rounded-xl text-xs font-semibold w-full text-slate-800',
                  { 'border-rose-500 focus:border-rose-500 focus:ring-rose-500': isConfirmPasswordTouched && !isConfirmPasswordValid }
                ]" 
              />
              <p v-if="isConfirmPasswordTouched && !isConfirmPasswordValid" class="text-[10px] text-rose-500 font-bold mt-1">Konfirmasi sandi tidak cocok dengan sandi baru.</p>
            </div>
          </div>

          <!-- Alert Notifications inside Form -->
          <div v-if="successMessage" class="alert alert-success rounded-xl py-2 px-3 text-xs font-bold text-emerald-800 bg-emerald-50 border-emerald-100 flex gap-2">
            <CheckCircle2 class="w-4 h-4 shrink-0 text-emerald-600" />
            <span>{{ successMessage }}</span>
          </div>

          <div v-if="errorMessage" class="alert alert-error rounded-xl py-2 px-3 text-xs font-bold flex gap-2">
            <AlertTriangle class="w-4 h-4 shrink-0" />
            <span>{{ errorMessage }}</span>
          </div>

          <!-- Submit Profile Updates button -->
          <div class="flex justify-end pt-2">
            <button 
              type="submit" 
              :disabled="isSaving" 
              class="btn bg-gradient-to-r from-emerald-500 to-teal-600 text-white font-bold border-none hover:from-emerald-600 hover:to-teal-700 rounded-xl px-6 min-h-0 h-10 shadow-md shadow-emerald-500/10"
            >
              <RefreshCw v-if="isSaving" class="w-4 h-4 animate-spin shrink-0" />
              <span v-else>Simpan Perubahan</span>
            </button>
          </div>
        </form>

      </div>
    </div>

    <!-- Danger Zone block -->
    <div class="bg-rose-50/50 rounded-3xl border border-rose-100/70 p-6 md:p-8 shadow-md">
      <div class="flex items-center justify-between flex-wrap gap-6 font-sans">
        <div class="max-w-md">
          <h3 class="text-base font-black text-rose-800 flex items-center gap-1.5 select-none">
            <ShieldAlert class="w-5 h-5 text-rose-600" />
            Zona Bahaya
          </h3>
          <p class="text-xs text-rose-700/80 font-bold mt-1 leading-relaxed">
            Menghapus akun Anda bersifat permanen. Seluruh data registrasi bisnis, ulasan SWOT kompetitor, dan riwayat rekening koran PDF Anda akan dihapus selamanya dari server.
          </p>
        </div>
        <div>
          <button @click="showDeleteModal = true" class="btn bg-rose-600 hover:bg-rose-700 border-none text-white font-bold rounded-xl px-6">
            <Trash2 class="w-4 h-4 shrink-0" /> Hapus Akun Saya
          </button>
        </div>
      </div>
    </div>

    <!-- DOUBLE CONFIRMATION DELETE MODAL -->
    <div v-if="showDeleteModal" class="modal modal-open backdrop-blur-sm z-50">
      <div class="modal-box bg-white border border-slate-200 shadow-2xl rounded-3xl max-w-md font-sans">
        
        <div class="text-center space-y-4 mb-6 select-none">
          <div class="w-12 h-12 rounded-2xl bg-rose-50 text-rose-600 flex items-center justify-center mx-auto shadow-sm">
            <ShieldAlert class="w-6 h-6" />
          </div>
          <h3 class="text-lg font-black text-slate-800">Apakah Anda Yakin?</h3>
          <p class="text-xs text-slate-500 font-bold leading-relaxed">
            Tindakan ini tidak dapat dibatalkan. Ketik kata kunci di bawah untuk mengonfirmasi penghapusan akun permanen Anda.
          </p>
        </div>

        <div class="form-control w-full space-y-3">
          <label class="label">
            <span class="label-text-alt font-black text-slate-600 text-[10px] uppercase tracking-wider">Ketik <span class="text-rose-600 font-black">HAPUS AKUN</span> untuk mengonfirmasi</span>
          </label>
          <input 
            type="text" 
            v-model="confirmDeleteText"
            placeholder="HAPUS AKUN"
            class="input input-bordered focus:border-rose-500 focus:ring-1 focus:ring-rose-500 rounded-xl text-center text-xs font-black text-slate-800" 
          />
        </div>

        <div v-if="deleteError" class="alert alert-error rounded-xl py-2 px-3 text-[10px] font-bold mt-4 flex gap-2">
          <AlertTriangle class="w-4 h-4 shrink-0" />
          <span>{{ deleteError }}</span>
        </div>

        <div class="modal-action flex justify-end gap-3 mt-6">
          <button @click="showDeleteModal = false; confirmDeleteText = ''; deleteError = '';" class="btn btn-ghost rounded-xl text-xs font-extrabold text-slate-500">
            Batalkan
          </button>
          <button @click="handleDeleteAccount" class="btn bg-rose-600 hover:bg-rose-700 border-none text-white font-bold rounded-xl text-xs px-6">
            Hapus Permanen
          </button>
        </div>

      </div>
    </div>

  </div>
</template>
