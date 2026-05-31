<script setup lang="ts">
import { ref } from 'vue';
import { useBusinessStore } from '../../stores/business';
import { useFinancialStore, type FinancialReport, TransactionType } from '../../stores/financial';
import { 
  UploadCloud, Trash2, FileText, CheckCircle2, XCircle, X, Landmark, Zap, RefreshCw
} from 'lucide-vue-next';

const businessStore = useBusinessStore();
const financialStore = useFinancialStore();

// Toggle upload container visibility state
const showUploadForm = ref(false);

// Max file size read from env config or default 10MB
const maxFileSize = Number(import.meta.env.VITE_MAX_FILE_SIZE) || 10 * 1024 * 1024;
const maxFileMb = maxFileSize / (1024 * 1024);

// Upload states
const fileInputRef = ref<HTMLInputElement | null>(null);
const selectedFile = ref<File | null>(null);
const fileError = ref('');
const showSuccessToast = ref(false);

// Detail explorer state
const activeDetailReport = ref<FinancialReport | null>(null);

function triggerFileInput() {
  fileInputRef.value?.click();
}

function handleFileChange(event: Event) {
  const target = event.target as HTMLInputElement;
  const files = target.files;
  fileError.value = '';

  if (files && files.length > 0) {
    const file = files[0];
    if (file.type !== 'application/pdf') {
      fileError.value = 'Hanya file PDF rekening koran yang didukung.';
      return;
    }
    if (file.size > maxFileSize) {
      fileError.value = `Ukuran file melebihi batas maksimal ${maxFileMb}MB.`;
      return;
    }
    selectedFile.value = file;
  }
}

function handleDrop(event: DragEvent) {
  fileError.value = '';
  const files = event.dataTransfer?.files;

  if (files && files.length > 0) {
    const file = files[0];
    if (file.type !== 'application/pdf') {
      fileError.value = 'Hanya file PDF rekening koran yang didukung.';
      return;
    }
    if (file.size > maxFileSize) {
      fileError.value = `Ukuran file melebihi batas maksimal ${maxFileMb}MB.`;
      return;
    }
    selectedFile.value = file;
  }
}

function cancelSelection() {
  selectedFile.value = null;
  if (fileInputRef.value) {
    fileInputRef.value.value = '';
  }
}

async function uploadFile() {
  if (!selectedFile.value || !businessStore.activeBusiness) return;
  
  try {
    await financialStore.uploadBankStatement(
      businessStore.activeBusiness.id,
      { name: selectedFile.value.name, size: selectedFile.value.size }
    );
    selectedFile.value = null;
    if (fileInputRef.value) {
      fileInputRef.value.value = '';
    }
    showSuccessToast.value = true;
    showUploadForm.value = false; // Hide form on successful upload
    setTimeout(() => {
      showSuccessToast.value = false;
    }, 3000);
  } catch (err) {
    console.error(err);
  }
}

function formatCurrency(val: number) {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(val);
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' });
}

function formatFullDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString('id-ID', { 
    day: 'numeric', 
    month: 'long', 
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

function handleDownloadCSV() {
  if (!activeDetailReport.value) return;
  const report = activeDetailReport.value;
  const headers = ['Tanggal', 'Referensi', 'Deskripsi', 'Kategori', 'Tipe', 'Jumlah', 'Saldo'];
  const rows = report.bank_statement.transactions.map(t => [
    new Date(t.date).toLocaleDateString('id-ID'),
    t.reference || '',
    t.description.replace(/"/g, '""'),
    t.category,
    t.type,
    t.amount,
    t.balance
  ]);
  
  const csvContent = "data:text/csv;charset=utf-8," 
    + [headers.join(','), ...rows.map(r => r.map(val => `"${val}"`).join(','))].join('\n');
    
  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", `Vantage_AI_Transaksi_${report.bank_statement.name.replace(/\s+/g, '_')}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

const extractingReportId = ref<string | null>(null);

async function triggerManualExtraction(report: FinancialReport) {
  if (extractingReportId.value) return;
  
  extractingReportId.value = report.id;
  report.status = 'processing';
  
  try {
    // Simulate real extraction processing
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Fill the empty transactions with mock parsed items if they were empty
    if (report.bank_statement.transactions.length === 0) {
      report.bank_statement.transactions = [
        {
          date: new Date().toISOString(),
          description: 'Ekstraksi Manual: Setoran Deposit Merchant QRIS',
          type: TransactionType.CREDIT,
          category: 'Pendapatan Operasional',
          subcategory: 'QRIS Settlement',
          amount: 8500000,
          balance: 23500000,
          reference: 'REF-MAN-01'
        },
        {
          date: new Date().toISOString(),
          description: 'Ekstraksi Manual: Pembayaran Biaya Listrik & Air',
          type: TransactionType.DEBIT,
          category: 'Beban Operasional (OPEX)',
          subcategory: 'Utilitas',
          amount: 1200000,
          balance: 22300000,
          reference: 'REF-MAN-02'
        }
      ];
      report.bank_statement.final_balance = 22300000;
    }
    
    report.status = 'completed';
    showSuccessToast.value = true;
    setTimeout(() => {
      showSuccessToast.value = false;
    }, 3000);
  } catch (err) {
    report.status = 'failed';
    console.error(err);
  } finally {
    extractingReportId.value = null;
  }
}
</script>

<template>
  <div class="space-y-8 font-sans">
    
    <!-- Empty state: If no business is registered -->
    <div v-if="!businessStore.activeBusiness" class="max-w-2xl mx-auto bg-white rounded-2xl border border-slate-200/80 p-12 text-center shadow-lg relative overflow-hidden select-none">
      <div class="absolute -top-12 -left-12 w-48 h-48 bg-emerald-500/5 blur-3xl rounded-full pointer-events-none"></div>
      <div class="space-y-6 max-w-md mx-auto">
        <div class="w-16 h-16 rounded-2xl bg-slate-50 border border-slate-100 text-slate-400 flex items-center justify-center mx-auto shadow-sm">
          <FileText class="w-8 h-8" />
        </div>
        <h2 class="text-2xl font-black text-slate-800">Menunggu Unggah Rekening</h2>
        <p class="text-sm text-slate-500 font-semibold leading-relaxed">
          Silakan daftarkan bisnis Anda terlebih dahulu untuk mengaktifkan portal unggah rekening koran.
        </p>
      </div>
    </div>

    <!-- Active State: Bank Statement Explorer -->
    <div v-else class="space-y-6">
      
      <!-- Toggleable PDF Upload Container -->
      <div 
        v-if="showUploadForm" 
        class="bg-white rounded-2xl border border-emerald-100 p-6 md:p-8 shadow-md space-y-6 animate-fade-in relative overflow-hidden"
      >
        <!-- Background aesthetic gradient blob -->
        <div class="absolute -top-10 -right-10 w-32 h-32 bg-emerald-500/5 blur-2xl rounded-full pointer-events-none"></div>

        <div class="flex items-center justify-between select-none relative z-10">
          <div class="space-y-1">
            <h3 class="text-base font-black text-slate-800 flex items-center gap-2">
              <UploadCloud class="w-5 h-5 text-emerald-600" />
              Unggah Rekening Koran PDF
            </h3>
            <p class="text-xs text-slate-550 font-bold leading-relaxed max-w-2xl mt-1">
              Vantage AI mengaudit data transaksi Anda secara terenkripsi. Ekstraksi otomatis memetakan pendapatan, beban pokok (COGS), pengeluaran operasional (OPEX), dan belanja modal (CAPEX).
            </p>
          </div>
          <button 
            @click="showUploadForm = false" 
            class="btn btn-ghost btn-circle btn-xs text-slate-400 hover:text-slate-600 self-start"
            title="Tutup panel"
          >
            <X class="w-4 h-4" />
          </button>
        </div>

        <!-- Drag & Drop container -->
        <div 
          @click="!selectedFile && !financialStore.isUploading ? triggerFileInput() : null"
          @dragover.prevent
          @drop.prevent="handleDrop"
          :class="[
            'border-2 border-dashed rounded-2xl p-10 text-center transition-all duration-200 relative group/drop select-none z-10',
            !selectedFile && !financialStore.isUploading 
              ? 'border-slate-200 hover:border-emerald-500/80 cursor-pointer hover:bg-slate-50/50' 
              : 'border-emerald-200/65 bg-emerald-50/5'
          ]"
        >
          <input 
            type="file" 
            ref="fileInputRef" 
            @change="handleFileChange" 
            accept="application/pdf" 
            class="hidden" 
          />
          
          <!-- Case 1: Ready to Pick (No file selected, not uploading) -->
          <div class="space-y-4" v-if="!selectedFile && !financialStore.isUploading">
            <div class="w-12 h-12 rounded-xl bg-slate-50 border border-slate-100 text-slate-450 group-hover/drop:text-emerald-500 flex items-center justify-center mx-auto shadow-xs transition-all duration-200 group-hover/drop:-translate-y-0.5">
              <UploadCloud class="w-6 h-6" />
            </div>
            <div class="space-y-1">
              <div class="text-xs font-black text-slate-700">Pilih berkas PDF atau seret ke sini</div>
              <div class="text-[10px] text-slate-500 font-bold">PDF Ukuran Maksimal {{ maxFileMb }}MB</div>
            </div>
          </div>

          <!-- Case 2: Selected & Awaiting Upload (File selected, not uploading) -->
          <div class="space-y-5 py-2" v-else-if="selectedFile && !financialStore.isUploading">
            <div class="w-14 h-14 rounded-2xl bg-emerald-50 border border-emerald-100 text-emerald-600 flex items-center justify-center mx-auto shadow-sm">
              <FileText class="w-7 h-7" />
            </div>
            <div class="space-y-1 max-w-md mx-auto">
              <div class="text-xs font-black text-slate-800 truncate px-4" :title="selectedFile.name">
                {{ selectedFile.name }}
              </div>
              <div class="text-[10px] text-slate-500 font-bold font-mono">
                {{ (selectedFile.size / (1024 * 1024)).toFixed(2) }} MB • Berkas Terpilih dan Siap Diunggah
              </div>
            </div>
            <div class="flex items-center justify-center gap-3 pt-2">
              <button 
                @click.stop="cancelSelection" 
                class="btn btn-sm bg-white hover:bg-slate-100 text-slate-700 border border-slate-200 rounded-xl px-4 font-black text-[10px] uppercase tracking-wider min-h-0 h-9 shadow-xs"
              >
                Hapus
              </button>
              <button 
                @click.stop="uploadFile" 
                class="btn btn-sm bg-emerald-600 hover:bg-emerald-700 text-white border-none rounded-xl px-5 font-black text-[10px] uppercase tracking-wider min-h-0 h-9 shadow-sm"
              >
                Mulai Unggah Rekening Koran
              </button>
            </div>
          </div>

          <!-- Case 3: Spinner during upload -->
          <div class="space-y-4 py-2" v-else>
            <div class="relative w-12 h-12 mx-auto">
              <div class="absolute inset-0 rounded-full border-4 border-slate-100"></div>
              <div class="absolute inset-0 rounded-full border-4 border-emerald-500 border-t-transparent animate-spin"></div>
            </div>
            <div class="space-y-2">
              <div class="text-xs font-black text-slate-750">Mengekstrak data rekening koran...</div>
              <div class="max-w-xs mx-auto bg-slate-100 rounded-full h-1.5 overflow-hidden">
                <div class="bg-emerald-500 h-full transition-all duration-300" :style="{ width: financialStore.uploadProgress + '%' }"></div>
              </div>
              <div class="text-[9px] text-slate-550 font-mono tracking-wide font-extrabold">{{ financialStore.uploadProgress }}% Selesai</div>
            </div>
          </div>
        </div>

        <div v-if="fileError" class="alert alert-error rounded-xl py-2.5 px-3 text-xs font-bold flex gap-2 max-w-md shadow-sm">
          <XCircle class="w-4 h-4 shrink-0" />
          <span>{{ fileError }}</span>
        </div>
      </div>

      <!-- Premium B2B Action Row above the table (Fix: pulled out of table header) -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs select-none gap-4">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center shrink-0 shadow-sm">
            <Landmark class="w-5 h-5" />
          </div>
          <div>
            <h4 class="text-xs font-black text-slate-850 uppercase tracking-wider">Kelola Berkas Rekening Koran</h4>
            <p class="text-[10px] text-slate-500 font-bold leading-relaxed">Unggah file PDF rekening koran Anda untuk otomatis melakukan ekstraksi audit likuiditas oleh Vantage AI.</p>
          </div>
        </div>
        <button 
          @click="showUploadForm = !showUploadForm"
          :class="[
            'btn btn-sm border rounded-xl gap-1.5 shadow-sm font-black text-[11px] uppercase tracking-wider transition-all duration-200 min-h-0 h-9 px-4 shrink-0',
            showUploadForm 
              ? 'bg-slate-100 hover:bg-slate-200 border-slate-250/70 text-slate-700' 
              : 'bg-emerald-600 hover:bg-emerald-700 text-white border-none'
          ]"
        >
          <UploadCloud class="w-4 h-4 shrink-0" />
          {{ showUploadForm ? 'Tutup Panel Unggah' : 'Tambah Rekening Koran' }}
        </button>
      </div>

      <!-- Extraction History records (Full Width) -->
      <div class="bg-white rounded-2xl border border-slate-200/80 overflow-hidden shadow-sm">
        <div class="px-6 py-4.5 border-b border-slate-100 flex items-center justify-between flex-wrap gap-4 select-none">
          <h3 class="text-base font-extrabold text-slate-800 flex items-center gap-2">
            <FileText class="w-5 h-5 text-emerald-600" />
            Riwayat Ekstraksi Rekening Koran
          </h3>
          <span class="badge bg-slate-50 border border-slate-200 text-slate-650 text-[10px] font-black uppercase tracking-wider px-2.5 py-1.5 rounded-md">
            Total: {{ financialStore.reports.length }} Berkas Terdeteksi
          </span>
        </div>

        <!-- Success Toast indicator -->
        <div v-if="showSuccessToast" class="m-6 mb-0 alert alert-success rounded-xl py-2.5 px-4 text-xs font-bold text-emerald-800 bg-emerald-50 border border-emerald-100 flex gap-2">
          <CheckCircle2 class="w-4 h-4 shrink-0 text-emerald-600" />
          <span>Rekening koran berhasil diunggah dan diekstrak!</span>
        </div>

        <div class="overflow-x-auto w-full">
          <table class="table w-full text-slate-700">
            <thead>
              <tr class="bg-slate-50 border-b border-slate-100 text-slate-400 text-[10px] font-black uppercase tracking-wider select-none">
                <th class="py-3 px-6 text-left">Nama Berkas</th>
                <th class="py-3 px-6 text-left">Pemilik Rekening</th>
                <th class="py-3 px-6 text-left">Periode Audit</th>
                <th class="py-3 px-6 text-right">Saldo Akhir</th>
                <th class="py-3 px-6 text-center">Status</th>
                <th class="py-3 px-6 text-center">Ekstraksi</th>
                <th class="py-3 px-6 text-center">Aksi</th>
              </tr>
            </thead>
            <tbody class="text-xs font-semibold">
              <tr v-if="financialStore.reports.length === 0">
                <td colspan="7" class="py-12 text-center text-slate-400 font-bold select-none">
                  Belum ada transaksi rekening koran yang tercatat. Silakan klik "Tambah Dokumen" di atas.
                </td>
              </tr>
              <tr 
                v-else 
                v-for="rep in financialStore.reports" 
                :key="rep.id" 
                class="hover:bg-slate-50/70 border-b border-slate-100/50 cursor-pointer"
                @click="activeDetailReport = rep"
              >
                <td class="py-4 px-6 font-bold text-slate-800 max-w-[160px] truncate">
                  <div class="flex items-center gap-2">
                    <FileText class="w-4 h-4 text-emerald-600 shrink-0" />
                    <span class="truncate">{{ rep.filename }}</span>
                  </div>
                </td>
                <td class="py-4 px-6 uppercase font-mono truncate max-w-[120px]">{{ rep.bank_statement.name }}</td>
                <td class="py-4 px-6 font-medium text-slate-500">
                  {{ formatDate(rep.bank_statement.period_start) }} - {{ formatDate(rep.bank_statement.period_end) }}
                </td>
                <td class="py-4 px-6 text-right font-black font-mono text-emerald-600">
                  {{ formatCurrency(rep.bank_statement.final_balance) }}
                </td>
                <td class="py-4 px-6 text-center select-none" @click.stop>
                  <span 
                    v-if="!rep.status || rep.status === 'success' || rep.status === 'completed'"
                    class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-black uppercase tracking-wider bg-emerald-50 text-emerald-700 border border-emerald-100"
                  >
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                    Selesai
                  </span>
                  <span 
                    v-else-if="rep.status === 'processing'"
                    class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-black uppercase tracking-wider bg-blue-50 text-blue-700 border border-blue-100"
                  >
                    <span class="w-1.5 h-1.5 rounded-full bg-blue-500 animate-spin"></span>
                    Memproses
                  </span>
                  <span 
                    v-else-if="rep.status === 'failed'"
                    class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-black uppercase tracking-wider bg-rose-50 text-rose-700 border border-rose-100"
                  >
                    <span class="w-1.5 h-1.5 rounded-full bg-rose-500"></span>
                    Gagal
                  </span>
                  <span 
                    v-else
                    class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-black uppercase tracking-wider bg-amber-50 text-amber-700 border border-amber-100"
                  >
                    <span class="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse"></span>
                    Tertunda
                  </span>
                </td>
                <td class="py-4 px-6 text-center select-none" @click.stop>
                  <div class="flex justify-center items-center">
                    <span 
                      v-if="!rep.status || rep.status === 'success' || rep.status === 'completed'"
                      class="text-[10px] text-slate-400 font-bold uppercase tracking-wider flex items-center justify-center gap-1"
                    >
                      <CheckCircle2 class="w-3.5 h-3.5 text-slate-400" />
                      Terestrak
                    </span>
                    <span 
                      v-else-if="rep.status === 'processing'"
                      class="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-[10px] font-bold text-blue-600 bg-blue-50 border border-blue-100 animate-pulse"
                    >
                      <RefreshCw class="w-3 h-3 text-blue-500 animate-spin" />
                      Proses...
                    </span>
                    <button 
                      v-else
                      @click="triggerManualExtraction(rep)" 
                      class="btn btn-xs bg-emerald-50 text-emerald-700 hover:bg-emerald-100 hover:text-emerald-850 border border-emerald-200 hover:border-emerald-300 rounded-lg px-2.5 py-1 font-black text-[10px] uppercase tracking-wider h-7 min-h-0"
                      title="Ekstrak ulang data dari rekening koran ini"
                    >
                      <Zap class="w-3 h-3 text-emerald-600 inline mr-1" />
                      Ekstrak
                    </button>
                  </div>
                </td>
                <td class="py-4 px-6 text-center" @click.stop>
                  <div class="flex items-center justify-center gap-1.5">
                    <button 
                      @click="activeDetailReport = rep" 
                      class="btn btn-ghost btn-xs text-emerald-600 hover:bg-emerald-50 rounded-lg px-2.5 font-bold"
                    >
                      Buka Detil
                    </button>
                    <button 
                      @click="financialStore.deleteReport(rep.id)" 
                      class="btn btn-ghost btn-circle btn-xs text-rose-500 hover:bg-rose-50"
                      title="Hapus record"
                    >
                      <Trash2 class="w-3.5 h-3.5" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>

    <!-- HIGH-FIDELITY DETAILED EXTRACTED DATA MODAL DRAWER -->
    <div v-if="activeDetailReport" class="modal modal-open backdrop-blur-xs z-50">
      <!-- Dimmed Background Backdrop (Click to Close) -->
      <div @click="activeDetailReport = null" class="absolute inset-0 bg-slate-950/60 transition-opacity duration-300"></div>
      
      <div class="modal-box bg-white border border-slate-200/90 shadow-2xl rounded-2xl max-w-5xl w-11/12 p-0 overflow-hidden flex flex-col max-h-[85vh] relative z-10 animate-scale-up">
        
        <!-- Modal Top Bar Header -->
        <div class="bg-slate-900 text-white px-6 py-4 flex items-center justify-between select-none">
          <div class="flex items-center gap-3">
            <Landmark class="w-5 h-5 text-emerald-400" />
            <div>
              <h3 class="text-sm font-extrabold tracking-wide">Eksplorasi Transaksi Terestrak</h3>
              <p class="text-[9px] text-slate-450 font-mono">ID Laporan: {{ activeDetailReport.id }} | Dibuat: {{ formatFullDate(activeDetailReport.created_at) }}</p>
            </div>
          </div>
          <button @click="activeDetailReport = null" class="btn btn-ghost btn-circle btn-sm text-slate-400 hover:text-white transition-colors duration-150">
            <X class="w-5 h-5" />
          </button>
        </div>

        <!-- Modal Content Scrollable -->
        <div class="p-6 md:p-8 overflow-y-auto space-y-6 flex-1 font-sans">
          
          <!-- Metrik Ringkasan Rekening Grid (Strict Equalized Column Widths) -->
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6 bg-slate-50 border border-slate-200/80 p-6 rounded-xl font-sans relative overflow-hidden select-none">
            <!-- Background aesthetic gradient blob -->
            <div class="absolute -top-10 -right-10 w-24 h-24 bg-emerald-500/5 blur-2xl rounded-full pointer-events-none"></div>

            <div class="space-y-1">
              <span class="text-[10px] font-black text-slate-500 uppercase tracking-widest block">Pemilik Rekening</span>
              <span class="text-xs font-extrabold text-slate-900 uppercase font-mono block leading-tight break-words select-all">{{ activeDetailReport.bank_statement.name }}</span>
            </div>
            <div class="space-y-1 sm:border-l sm:border-slate-200/80 sm:pl-6">
              <span class="text-[10px] font-black text-slate-500 uppercase tracking-widest block">Nomor Rekening</span>
              <span class="text-xs font-extrabold text-slate-900 font-mono block leading-tight break-all select-all">{{ activeDetailReport.bank_statement.account_number }}</span>
            </div>
            <div class="space-y-1 md:border-l md:border-slate-200/80 md:pl-6">
              <span class="text-[10px] font-black text-slate-500 uppercase tracking-widest block">Saldo Awal Periode</span>
              <span class="text-xs font-extrabold text-slate-700 font-mono block leading-tight">{{ formatCurrency(activeDetailReport.bank_statement.initial_balance) }}</span>
            </div>
            <div class="space-y-1 sm:border-l sm:border-slate-200/80 sm:pl-6">
              <span class="text-[10px] font-black text-slate-500 uppercase tracking-widest block">Saldo Akhir Periode</span>
              <span class="text-xs font-extrabold text-emerald-600 font-mono block leading-tight">{{ formatCurrency(activeDetailReport.bank_statement.final_balance) }}</span>
            </div>
          </div>

          <!-- Transaction List Section -->
          <div class="space-y-3.5">
            <div class="flex items-center justify-between border-b border-slate-100 pb-2 select-none">
              <h4 class="text-[11px] font-black text-slate-800 uppercase tracking-wider">
                Daftar Detail Transaksi ({{ activeDetailReport.bank_statement.transactions.length }} Data Terdeteksi)
              </h4>
              <span class="text-[10px] text-slate-500 font-bold font-mono">
                Periode: {{ formatDate(activeDetailReport.bank_statement.period_start) }} - {{ formatDate(activeDetailReport.bank_statement.period_end) }}
              </span>
            </div>

            <!-- Transaction Table Container (With Max Height for Sticky Header Scrolling) -->
            <div class="overflow-x-auto overflow-y-auto w-full max-h-[380px] rounded-xl border border-slate-200/80 relative shadow-sm">
              <table class="table table-zebra table-sm w-full text-slate-700 border-separate border-spacing-0">
                <!-- Sticky Table Head -->
                <thead class="sticky top-0 z-10 bg-slate-100/95 backdrop-blur-xs shadow-sm">
                  <tr class="text-slate-500 text-[9px] font-black uppercase tracking-wider select-none">
                    <th class="bg-slate-100 py-3 px-4 text-left w-[11%] border-b border-slate-200">Tanggal</th>
                    <th class="bg-slate-100 py-3 px-4 text-left w-[12%] border-b border-slate-200">Referensi</th>
                    <th class="bg-slate-100 py-3 px-4 text-left w-[40%] border-b border-slate-200">Keterangan Deskripsi</th>
                    <th class="bg-slate-100 py-3 px-4 text-left w-[15%] border-b border-slate-200">Klasifikasi Kategori</th>
                    <th class="bg-slate-100 py-3 px-4 text-right w-[11%] border-b border-slate-200">Jumlah</th>
                    <th class="bg-slate-100 py-3 px-4 text-right w-[11%] border-b border-slate-200">Saldo Buku</th>
                  </tr>
                </thead>
                <tbody class="text-[11px] font-semibold">
                  <tr v-for="(txn, idx) in activeDetailReport.bank_statement.transactions" :key="'txn-'+idx" class="hover:bg-slate-50/50 transition-colors duration-100">
                    <td class="py-3 px-4 text-slate-500 font-medium font-mono whitespace-nowrap w-[11%] border-b border-slate-100">
                      {{ new Date(txn.date).toLocaleDateString('id-ID', { day: '2-digit', month: '2-digit', year: 'numeric' }) }}
                    </td>
                    <td class="py-3 px-4 text-slate-400 font-mono font-medium w-[12%] truncate border-b border-slate-100">{{ txn.reference || '-' }}</td>
                    <td class="py-3 px-4 font-bold text-slate-800 w-[40%] max-w-[320px] truncate border-b border-slate-100" :title="txn.description">
                      {{ txn.description }}
                    </td>
                    <td class="py-3 px-4 w-[15%] border-b border-slate-100">
                      <!-- Content Clipping Fix: use custom inline-flex badge -->
                      <span 
                        :class="[
                          'inline-flex items-center justify-center whitespace-nowrap rounded-lg text-[9px] font-black uppercase tracking-wider px-2.5 py-1 border transition-colors duration-150',
                          txn.category.includes('Pendapatan') 
                            ? 'bg-emerald-50 text-emerald-700 border-emerald-100' 
                            : (txn.category.includes('OPEX') || txn.category.includes('COGS') 
                                ? 'bg-rose-50 text-rose-700 border-rose-100' 
                                : 'bg-slate-50 text-slate-650 border-slate-200')
                        ]"
                        :title="txn.category"
                      >
                        {{ txn.category }}
                      </span>
                    </td>
                    <td class="py-3 px-4 text-right font-black font-mono w-[11%] border-b border-slate-100">
                      <span :class="txn.type === TransactionType.CREDIT ? 'text-emerald-600' : 'text-rose-600'">
                        {{ txn.type === TransactionType.CREDIT ? '+' : '-' }}{{ formatCurrency(txn.amount) }}
                      </span>
                    </td>
                    <td class="py-3 px-4 text-right font-black font-mono text-slate-800 w-[11%] border-b border-slate-100">
                      {{ formatCurrency(txn.balance) }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>

        <!-- Footer (Consistent Padding, Aligned to the Bottom Right, Secondary CSV Action) -->
        <div class="bg-slate-50 border-t border-slate-200/80 px-6 py-4 flex items-center justify-between select-none">
          <div class="text-[10px] text-slate-400 font-bold hidden sm:block">
            Vantage AI Secure Financial Portal
          </div>
          <div class="flex items-center gap-3 ml-auto">
            <button 
              @click="handleDownloadCSV" 
              class="btn btn-sm btn-outline border-slate-200 text-slate-700 hover:bg-slate-100 hover:text-slate-900 rounded-lg px-4 font-black text-[11px] uppercase tracking-wider"
            >
              Unduh Laporan (CSV)
            </button>
            <button 
              @click="activeDetailReport = null" 
              class="btn btn-sm bg-slate-900 hover:bg-slate-800 text-white border-none rounded-lg px-6 font-black text-[11px] uppercase tracking-wider shadow-sm"
            >
              Tutup Eksplorer
            </button>
          </div>
        </div>

      </div>
    </div>

  </div>
</template>
