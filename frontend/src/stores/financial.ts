import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const TransactionType = {
  CREDIT: 'credit',
  DEBIT: 'debit'
} as const;
export type TransactionType = typeof TransactionType[keyof typeof TransactionType];

export const TransactionCategory = {
  PENDAPATAN_OPERASIONAL: "Pendapatan Operasional",
  PENDAPATAN_NON_OPERASIONAL: "Pendapatan Non-Operasional",
  INFLOW_NON_PENDAPATAN: "Inflow Non-Pendapatan",
  COGS: "Beban Pokok Penjualan (COGS)",
  OPEX: "Beban Operasional (OPEX)",
  CAPEX: "Belanja Modal (CAPEX)",
  BEBAN_NON_OPERASIONAL: "Beban Non-Operasional",
  OUTFLOW_NON_BEBAN: "Outflow Non-Beban",
  UNCLASSIFIED: "Belum Terklasifikasi"
} as const;
export type TransactionCategory = typeof TransactionCategory[keyof typeof TransactionCategory];

export const FinancialHealth = {
  VERY_HEALTHY: "very_healthy",
  HEALTHY: "healthy",
  MODERATE: "moderate",
  AT_RISK: "at_risk",
  DISTRESSED: "distressed"
} as const;
export type FinancialHealth = typeof FinancialHealth[keyof typeof FinancialHealth];

export interface Transaction {
  date: string;
  description: string;
  type: TransactionType;
  category: TransactionCategory;
  subcategory: string | null;
  amount: number;
  balance: number;
  reference: string | null;
}

export interface BankStatement {
  name: string;
  account_number: string;
  period_start: string;
  period_end: string;
  currency: string;
  initial_balance: number;
  final_balance: number;
  transactions: Transaction[];
}

export interface FinancialReport {
  id: string;
  business_id: string;
  owner_uid: string;
  file_url: string;
  bank_statement: BankStatement;
  generated_at: string;
  created_at: string;
  filename: string;
}

export interface FinancialAnalysis {
  report_id: string;
  insights: string[];
  warnings: string[];
  health_score: number;
  health_status: FinancialHealth;
  recommendations: string[];
}

export const useFinancialStore = defineStore('financial', () => {
  const reports = ref<FinancialReport[]>([]);
  const analysis = ref<FinancialAnalysis | null>(null);
  const loading = ref(false);
  const uploadProgress = ref(0);
  const isUploading = ref(false);
  const error = ref<string | null>(null);

  // Computed totals based on reports
  const activeReport = computed(() => reports.value[0] || null);

  const totalInflow = computed(() => {
    if (!activeReport.value) return 0;
    return activeReport.value.bank_statement.transactions
      .filter(t => t.type === TransactionType.CREDIT)
      .reduce((sum, t) => sum + t.amount, 0);
  });

  const totalOutflow = computed(() => {
    if (!activeReport.value) return 0;
    return activeReport.value.bank_statement.transactions
      .filter(t => t.type === TransactionType.DEBIT)
      .reduce((sum, t) => sum + t.amount, 0);
  });

  const netCashFlow = computed(() => totalInflow.value - totalOutflow.value);

  // Grouped by Category totals for active report
  const categoryTotals = computed(() => {
    const totals: Record<string, number> = {};
    if (!activeReport.value) return totals;

    // Initialize all categories with 0 for UI consistency
    Object.values(TransactionCategory).forEach(cat => {
      totals[cat] = 0;
    });

    activeReport.value.bank_statement.transactions.forEach(t => {
      totals[t.category] += t.amount;
    });

    return totals;
  });

  // Grouped by Category and Subcategory totals for active report
  const subcategoryTotals = computed(() => {
    const totals: Record<string, Record<string, number>> = {};
    if (!activeReport.value) return totals;

    activeReport.value.bank_statement.transactions.forEach(t => {
      const cat = t.category;
      const subcat = t.subcategory || 'Lainnya';
      const amt = t.amount;

      if (!totals[cat]) {
        totals[cat] = {};
      }
      if (!totals[cat][subcat]) {
        totals[cat][subcat] = 0;
      }
      totals[cat][subcat] += amt;
    });

    return totals;
  });

  // Calculate daily balances for visual charts
  const dailyBalances = computed(() => {
    if (!activeReport.value) return [];
    
    // Group transactions by date
    const transactions = activeReport.value.bank_statement.transactions;
    const dailyData: Record<string, { income: number; expenses: number; lastBalance: number }> = {};

    // Sort by date ascending to build sequence
    const sortedTxns = [...transactions].sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

    sortedTxns.forEach(t => {
      const dateStr = t.date.split('T')[0];
      if (!dailyData[dateStr]) {
        dailyData[dateStr] = { income: 0, expenses: 0, lastBalance: t.balance };
      }
      
      if (t.type === TransactionType.CREDIT) {
        dailyData[dateStr].income += t.amount;
      } else {
        dailyData[dateStr].expenses += t.amount;
      }
      dailyData[dateStr].lastBalance = t.balance;
    });

    return Object.entries(dailyData).map(([date, data]) => ({
      date,
      income: data.income,
      expenses: data.expenses,
      balance: data.lastBalance
    })).sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
  });

  function loadDemoData() {
    const now = new Date();
    const currentYear = now.getFullYear();
    const currentMonth = String(now.getMonth() + 1).padStart(2, '0');

    // Create 30 days of transactions for premium charting
    const mockTransactions: Transaction[] = [];
    let rollingBalance = 24500000; // Starting balance

    for (let day = 1; day <= 28; day++) {
      const dayStr = String(day).padStart(2, '0');
      const dateStr = `${currentYear}-${currentMonth}-${dayStr}T10:00:00Z`;

      // Operational Income on specific days (1st, 10th, 18th, 25th)
      if ([1, 10, 18, 25].includes(day)) {
        const incomeAmount = day === 1 ? 15000000 : (day === 10 ? 8500000 : (day === 18 ? 6200000 : 9800000));
        rollingBalance += incomeAmount;
        mockTransactions.push({
          date: dateStr,
          description: `Pembayaran Invoice Pelanggan #${day}`,
          type: TransactionType.CREDIT,
          category: TransactionCategory.PENDAPATAN_OPERASIONAL,
          subcategory: 'Penjualan Kopi & Makanan',
          amount: incomeAmount,
          balance: rollingBalance,
          reference: `REF-INV-${currentYear}${dayStr}`
        });
      }

      // Rent and Fixed Costs (COGS/OPEX) on 2nd and 5th
      if (day === 2) {
        const rentAmount = 6000000;
        rollingBalance -= rentAmount;
        mockTransactions.push({
          date: dateStr,
          description: 'Sewa Area Bulanan Ruko Senopati',
          type: TransactionType.DEBIT,
          category: TransactionCategory.OPEX,
          subcategory: 'Sewa Gedung',
          amount: rentAmount,
          balance: rollingBalance,
          reference: `REF-RENT-${currentYear}`
        });
      }

      if (day === 5) {
        const rawMaterials = 4500000;
        rollingBalance -= rawMaterials;
        mockTransactions.push({
          date: dateStr,
          description: 'Pembelian Biji Kopi Toraja & Arabika Premium',
          type: TransactionType.DEBIT,
          category: TransactionCategory.COGS,
          subcategory: 'Bahan Baku',
          amount: rawMaterials,
          balance: rollingBalance,
          reference: `REF-SUPP-A`
        });
      }

      // Operational and Utilities daily
      if (day % 4 === 0) {
        const opexAmount = 850000;
        rollingBalance -= opexAmount;
        mockTransactions.push({
          date: dateStr,
          description: 'Biaya Listrik, Wifi, Air & Kebersihan',
          type: TransactionType.DEBIT,
          category: TransactionCategory.OPEX,
          subcategory: 'Utilitas',
          amount: opexAmount,
          balance: rollingBalance,
          reference: `REF-UTIL-${day}`
        });
      }

      // Gaji Karyawan on 28th
      if (day === 28) {
        const salaries = 9500000;
        rollingBalance -= salaries;
        mockTransactions.push({
          date: dateStr,
          description: 'Gaji Bulanan Staff Barista & Kitchen',
          type: TransactionType.DEBIT,
          category: TransactionCategory.OPEX,
          subcategory: 'Gaji Karyawan',
          amount: salaries,
          balance: rollingBalance,
          reference: `REF-SAL-${currentMonth}`
        });
      }

      // Small incidental credit/debit
      if (day % 7 === 0) {
        const bankInterest = 75000;
        rollingBalance += bankInterest;
        mockTransactions.push({
          date: dateStr,
          description: 'Bunga Rekening Bank Bulanan',
          type: TransactionType.CREDIT,
          category: TransactionCategory.PENDAPATAN_NON_OPERASIONAL,
          subcategory: 'Pendapatan Bunga',
          amount: bankInterest,
          balance: rollingBalance,
          reference: `REF-INT-${day}`
        });
      }
    }

    reports.value = [
      {
        id: 'rep_01',
        business_id: 'biz_01',
        owner_uid: 'user_default',
        file_url: 'https://storage.googleapis.com/vantage-ai/statements/rek_mei_2026.pdf',
        filename: 'Rekening_Koran_Mei_2026.pdf',
        generated_at: new Date().toISOString(),
        created_at: new Date().toISOString(),
        bank_statement: {
          name: 'KOPI NUSANTARA SENOPATI',
          account_number: '124-00-98218-12',
          period_start: `${currentYear}-${currentMonth}-01T00:00:00Z`,
          period_end: `${currentYear}-${currentMonth}-28T23:59:59Z`,
          currency: 'IDR',
          initial_balance: 24500000,
          final_balance: rollingBalance,
          transactions: mockTransactions
        }
      }
    ];

    analysis.value = {
      report_id: 'rep_01',
      health_score: 82.5,
      health_status: FinancialHealth.VERY_HEALTHY,
      insights: [
        'Pendapatan Operasional Anda menunjukkan pola stabil dengan lonjakan sehat di akhir pekan.',
        'Margin kontribusi produk utama (Kopi Manual Brew) sangat tinggi mencapai 74%, mengindikasikan efisiensi COGS.',
        'Arus kas bersih bulanan bernilai positif (+IDR 12,925,000) yang memperkuat cadangan kas operasional.'
      ],
      warnings: [
        'Beban Operasional (OPEX) terutama untuk utilitas dan biaya sewa menyerap hampir 35% total pendapatan kotor.',
        'Saldo mengendap di rekening giro tidak menghasilkan imbal hasil optimal dibandingkan instrumen pasar uang.'
      ],
      recommendations: [
        'Pertahankan rasio kas minimal setara dengan 3 bulan biaya operasional tetap (sekitar IDR 40,000,000).',
        'Negosiasikan kontrak sewa jangka panjang dengan pemilik ruko untuk menghindari potensi kenaikan sewa tahun depan.',
        'Pindahkan surplus saldo di atas cadangan darurat ke deposito berjangka atau reksa dana pasar uang untuk mengoptimalkan bunga.'
      ]
    };
  }

  // Simulate PDF Bank Statement upload & parsing flow
  async function uploadBankStatement(businessId: string, file: { name: string; size: number }) {
    isUploading.value = true;
    uploadProgress.value = 0;
    error.value = null;

    try {
      // Simulate progressive upload
      for (let i = 1; i <= 10; i++) {
        await new Promise(resolve => setTimeout(resolve, 150));
        uploadProgress.value = i * 10;
      }

      // Simulate API call delay for parsing
      await new Promise(resolve => setTimeout(resolve, 1000));

      const now = new Date();
      const mockTransactions: Transaction[] = [
        {
          date: now.toISOString(),
          description: 'Pembayaran Deposit Awal Merchant QRIS',
          type: TransactionType.CREDIT,
          category: TransactionCategory.PENDAPATAN_OPERASIONAL,
          subcategory: 'QRIS Settlement',
          amount: 5000000,
          balance: 5000000,
          reference: 'REF-NEW-01'
        },
        {
          date: now.toISOString(),
          description: 'Pembelian Inventaris Alat Dapur & Cangkir',
          type: TransactionType.DEBIT,
          category: TransactionCategory.CAPEX,
          subcategory: 'Peralatan Cafe',
          amount: 1500000,
          balance: 3500000,
          reference: 'REF-NEW-02'
        }
      ];

      const newReport: FinancialReport = {
        id: 'rep_' + Math.random().toString(36).substr(2, 9),
        business_id: businessId,
        owner_uid: 'user_default',
        file_url: 'https://storage.googleapis.com/vantage-ai/statements/' + encodeURIComponent(file.name),
        filename: file.name,
        generated_at: now.toISOString(),
        created_at: now.toISOString(),
        bank_statement: {
          name: 'NEWLY PROCESSED BUSINESS',
          account_number: '888-21-990-12',
          period_start: now.toISOString(),
          period_end: now.toISOString(),
          currency: 'IDR',
          initial_balance: 0,
          final_balance: 3500000,
          transactions: mockTransactions
        }
      };

      // Add to beginning of reports array
      reports.value.unshift(newReport);

      // Generate analysis conforming to FinancialAnalysis schema
      analysis.value = {
        report_id: newReport.id,
        health_score: 68.0,
        health_status: FinancialHealth.MODERATE,
        insights: [
          'Laporan baru terdeteksi. Kas awal bernilai nol dan telah diisi deposit awal merchant.',
          'Pengeluaran modal (CAPEX) pertama dilakukan untuk pembelian peralatan dapur senilai IDR 1,500,000.'
        ],
        warnings: [
          'Pemasukan Anda masih sangat bergantung pada satu sumber transaksi deposit tunggal.',
          'Arus kas belum terdiversifikasi.'
        ],
        recommendations: [
          'Segera hubungkan dengan POS penjualan kasir untuk melacak transaksi harian.',
          'Siapkan dana kas kecil (petty cash) terpisah dari rekening operasional utama.'
        ]
      };

      return newReport;
    } catch (err: any) {
      error.value = err.message || 'Gagal mengunggah bank statement.';
      throw err;
    } finally {
      isUploading.value = false;
      uploadProgress.value = 0;
    }
  }

  function deleteReport(reportId: string) {
    reports.value = reports.value.filter(r => r.id !== reportId);
    if (reports.value.length === 0) {
      analysis.value = null;
    } else {
      // Re-link analysis to first report
      analysis.value = {
        report_id: reports.value[0].id,
        health_score: 82.5,
        health_status: FinancialHealth.VERY_HEALTHY,
        insights: [
          'Pendapatan Operasional Anda menunjukkan pola stabil dengan lonjakan sehat di akhir pekan.',
          'Margin kontribusi produk utama (Kopi Manual Brew) sangat tinggi mencapai 74%.'
        ],
        warnings: [
          'Beban Operasional menyerap 35% total pendapatan kotor.'
        ],
        recommendations: [
          'Pertahankan rasio kas minimal setara dengan 3 bulan biaya operasional.'
        ]
      };
    }
  }

  return {
    reports,
    analysis,
    loading,
    uploadProgress,
    isUploading,
    error,
    activeReport,
    totalInflow,
    totalOutflow,
    netCashFlow,
    categoryTotals,
    subcategoryTotals,
    dailyBalances,
    loadDemoData,
    uploadBankStatement,
    deleteReport
  };
});
