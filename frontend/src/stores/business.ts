import { defineStore } from 'pinia';
import { ref } from 'vue';

export interface Location {
  address: string;
  subdistrict: string;
  city: string;
  state: string;
  country: string;
  latitude: number;
  longitude: number;
}

export interface BusinessAnalysis {
  analysis_date: string;
  sentiment: string;
  top_positive_reviews: string[];
  top_negative_reviews: string[];
  strengths: string[];
  weaknesses: string[];
  opportunities: string[];
  threats: string[];
}

export interface Business {
  id: string;
  owner_uid: string;
  name: string;
  industry: string;
  google_maps_url: string;
  google_maps_rating: number;
  google_maps_number_of_reviews: number;
  location: Location;
  analysis?: BusinessAnalysis[];
}

export const CompetitorType = {
  DIRECT: "Direct",
  INDIRECT: "Indirect",
  REPLACEMENT: "Replacement"
} as const;
export type CompetitorType = typeof CompetitorType[keyof typeof CompetitorType];

export interface Competitor {
  id: string;
  business_id: string;
  owner_uid: string;
  name: string;
  industry: string;
  google_maps_rating: number;
  google_maps_number_of_reviews: number;
  google_maps_url: string;
  competitor_type: CompetitorType;
  location: Location;
  competitor_analysis?: BusinessAnalysis[];
  analysis_date: string;
}

export const useBusinessStore = defineStore('business', () => {
  const activeBusiness = ref<Business | null>(null);
  const competitors = ref<Competitor[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // Initialize with dummy data matching backend schemas
  function loadDemoData() {
    activeBusiness.value = {
      id: 'biz_01',
      owner_uid: 'user_default',
      name: 'Kopi Nusantara Senopati',
      industry: 'Food & Beverage',
      google_maps_url: 'https://maps.google.com/?q=Kopi+Nusantara+Senopati',
      google_maps_rating: 4.7,
      google_maps_number_of_reviews: 428,
      location: {
        address: 'Jl. Senopati No. 41, Kebayoran Baru',
        subdistrict: 'Kebayoran Baru',
        city: 'Jakarta Selatan',
        state: 'DKI Jakarta',
        country: 'Indonesia',
        latitude: -6.2243,
        longitude: 106.8085
      },
      analysis: [
        {
          analysis_date: new Date().toISOString(),
          sentiment: 'Sangat Positif. Dikenal dengan cita rasa kopi lokal premium, suasana cozy untuk WFH, dan barista yang sangat ramah. Sebagian kecil ulasan negatif mengeluhkan keterbatasan slot parkir.',
          top_positive_reviews: [
            '"Kopi Gula Aren di sini rasanya khas, biji kopinya terasa fresh. Tempatnya estetik dan tenang buat meeting!"',
            '"Pelayanan cepat dan ramah sekali. Croissant hangat dipadukan dengan latte adalah kombo sempurna di sini."',
            '"Internet kencang, banyak colokan, kursi ergonomis. Recommended place buat WFC di daerah Senopati!"'
          ],
          top_negative_reviews: [
            '"Parkirannya sempit sekali, susah kalau bawa mobil di jam makan siang."',
            '"Harga relatif premium dibanding kedai kopi lokal sekitarnya."',
            '"Di akhir pekan antriannya cukup panjang sehingga agak bising."'
          ],
          strengths: [
            'Biji kopi arabika single-origin pilihan langsung dari petani lokal',
            'Desain interior minimalis-modern dengan akustik peredam suara (sangat cocok untuk WFC)',
            'Lokasi premium di jantung pusat kuliner Senopati, Jakarta Selatan'
          ],
          weaknesses: [
            'Ketersediaan lahan parkir sangat minim (hanya muat 3 mobil)',
            'Stok produk bakery pendamping sering habis sebelum sore hari',
            'Ketergantungan tinggi pada satu supplier biji kopi Toraja utama'
          ],
          opportunities: [
            'Meluncurkan produk kopi kaleng siap minum (ready-to-drink) untuk retail',
            'Program katering mingguan/langganan ke gedung perkantoran SCBD terdekat',
            'Mengadakan workshop pembuatan kopi (manual brew class) berbayar di akhir pekan'
          ],
          threats: [
            'Persaingan langsung yang ketat dari coffee shop raksasa seperti Starbucks dan Kenangan',
            'Fluktuasi harga komoditas biji kopi mentah akibat cuaca tidak menentu',
            'Rencana pelebaran jalan yang berpotensi mengurangi area teras depan kedai'
          ]
        }
      ]
    };

    competitors.value = [
      {
        id: 'comp_01',
        business_id: 'biz_01',
        owner_uid: 'user_default',
        name: 'Starbucks Reserve Senopati',
        industry: 'Food & Beverage',
        google_maps_rating: 4.6,
        google_maps_number_of_reviews: 1420,
        google_maps_url: 'https://maps.google.com/?q=Starbucks+Reserve+Senopati',
        competitor_type: CompetitorType.DIRECT,
        analysis_date: new Date().toISOString(),
        location: {
          address: 'Jl. Senopati No. 82, Kebayoran Baru',
          subdistrict: 'Kebayoran Baru',
          city: 'Jakarta Selatan',
          state: 'DKI Jakarta',
          country: 'Indonesia',
          latitude: -6.2255,
          longitude: 106.8110
        },
        competitor_analysis: [
          {
            analysis_date: new Date().toISOString(),
            sentiment: 'Sangat Populer. Dikenal luas secara global dengan area parkir valet yang memadai dan area duduk luar ruangan yang besar.',
            top_positive_reviews: [
              '"Tempatnya megah banget, service khas Starbucks Reserve yang selalu memuaskan."',
              '"Nyaman buat nongkrong sore di lantai dua. Parkir luas karena ada valet."'
            ],
            top_negative_reviews: [
              '"Kopinya mahal sekali dan rasanya cenderung seragam dibanding specialty coffee."',
              '"Terlalu ramai dan bising di jam pulang kantor, tidak kondusif buat fokus kerja."'
            ],
            strengths: [
              'Kekuatan merk global (global brand awareness) yang tak tertandingi',
              'Lahan parkir memadai dengan fasilitas valet parkir gratis/berbayar',
              'Program loyalitas pelanggan (rewards) terintegrasi secara digital'
            ],
            weaknesses: [
              'Pricing strategy sangat mahal dibanding lokal brand',
              'Karakter rasa kopi kurang disukai oleh pencinta specialty manual-brew kopi lokal',
              'Layanan terkesan transaksional/kurang intim'
            ],
            opportunities: [
              'Kolaborasi musiman dengan seniman lokal untuk merchandise'
            ],
            threats: [
              'Pergeseran minat konsumen muda ke brand kopi lokal independen'
            ]
          }
        ]
      },
      {
        id: 'comp_02',
        business_id: 'biz_01',
        owner_uid: 'user_default',
        name: 'Kopi Kenangan Heritage Senayan',
        industry: 'Food & Beverage',
        google_maps_rating: 4.5,
        google_maps_number_of_reviews: 890,
        google_maps_url: 'https://maps.google.com/?q=Kopi+Kenangan+Heritage+Senayan',
        competitor_type: CompetitorType.DIRECT,
        analysis_date: new Date().toISOString(),
        location: {
          address: 'Senayan City Mall GF, Jl. Asia Afrika',
          subdistrict: 'Tanah Abang',
          city: 'Jakarta Pusat',
          state: 'DKI Jakarta',
          country: 'Indonesia',
          latitude: -6.2225,
          longitude: 106.8060
        },
        competitor_analysis: [
          {
            analysis_date: new Date().toISOString(),
            sentiment: 'Positif. Terkenal dengan variasi minuman kopi gula aren premium dan roti aneka rasa (Roti Kenangan).',
            top_positive_reviews: [
              '"Rasa Kopi Kenangan Mantan premium di outlet Heritage ini mantap sekali."',
              '"Tempatnya luas, pelayanan cepat lewat order aplikasi handphone."'
            ],
            top_negative_reviews: [
              '"Suasana mal kurang privat buat ngobrol serius."',
              '"Hampir selalu ramai antrian ojek online jadi agak bising di depan kasir."'
            ],
            strengths: [
              'Penyajian super cepat berbasis aplikasi pemesanan modern',
              'Harga yang sangat kompetitif dengan promosi berkala yang agresif',
              'Pilihan snack pendamping (Roti & Toast) yang bervariasi'
            ],
            weaknesses: [
              'Kenyamanan meja kerja terbatas (layout kedai lebih difokuskan untuk take-away/quick dine)',
              'Kurang menonjolkan edukasi asal-usul biji kopi (storytelling)'
            ],
            opportunities: [
              'Ekspansi variasi menu sehat rendah kalori/susu oat'
            ],
            threats: [
              'Kejenuhan pasar pada minuman kopi manis berbasis sirup'
            ]
          }
        ]
      },
      {
        id: 'comp_03',
        business_id: 'biz_01',
        owner_uid: 'user_default',
        name: 'Point Coffee Indomaret Senopati',
        industry: 'Food & Beverage',
        google_maps_rating: 4.3,
        google_maps_number_of_reviews: 120,
        google_maps_url: 'https://maps.google.com/?q=Point+Coffee+Indomaret+Senopati',
        competitor_type: CompetitorType.INDIRECT,
        analysis_date: new Date().toISOString(),
        location: {
          address: 'Indomaret Hybrid Senopati, Kebayoran Baru',
          subdistrict: 'Kebayoran Baru',
          city: 'Jakarta Selatan',
          state: 'DKI Jakarta',
          country: 'Indonesia',
          latitude: -6.2270,
          longitude: 106.8095
        },
        competitor_analysis: [
          {
            analysis_date: new Date().toISOString(),
            sentiment: 'Cukup Bagus. Fokus pada kenyamanan belanja sekalian beli kopi berkualitas mesin otomatis espresso dengan harga murah.',
            top_positive_reviews: [
              '"Kopinya murah tapi rasanya tidak kalah dengan cafe mahal. Beli lewat drive-thru praktis sekali."',
              '"Suka sama menu Frappe-nya, manisnya pas buat temen perjalanan."'
            ],
            top_negative_reviews: [
              '"Tidak cocok buat nongkrong, cuma ada 2 meja kecil di teras Indomaret."',
              '"Terkadang barista merangkap kasir minimarket jadi agak lama dilayani."'
            ],
            strengths: [
              'Harga sangat ramah di kantong mahasiswa/pekerja kantoran',
              'Sinergi lokasi terintegrasi dengan jaringan minimarket terbesar',
              'Layanan pesan-ambil praktis tanpa harus turun dari kendaraan (drive-thru)'
            ],
            weaknesses: [
              'Fasilitas dine-in sangat terbatas atau hampir tidak ada',
              'Variasi specialty single-origin kopi premium absen'
            ],
            opportunities: [
              'Menyediakan kemasan botolan ukuran 1 liter untuk konsumsi rumahan'
            ],
            threats: [
              'Munculnya coffee booth tandingan di jaringan minimarket kompetitor'
            ]
          }
        ]
      }
    ];
  }

  // Business CRUD
  async function createBusiness(name: string, industry: string, googleMapsUrl: string) {
    loading.value = true;
    error.value = null;
    try {
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 800));
      
      const newBiz: Business = {
        id: 'biz_' + Math.random().toString(36).substr(2, 9),
        owner_uid: 'user_default',
        name,
        industry,
        google_maps_url: googleMapsUrl,
        google_maps_rating: 4.5,
        google_maps_number_of_reviews: 1,
        location: {
          address: 'Jl. Senopati Raya, Kebayoran Baru',
          subdistrict: 'Kebayoran Baru',
          city: 'Jakarta Selatan',
          state: 'DKI Jakarta',
          country: 'Indonesia',
          latitude: -6.2240 + (Math.random() - 0.5) * 0.005,
          longitude: 106.8080 + (Math.random() - 0.5) * 0.005
        },
        analysis: [
          {
            analysis_date: new Date().toISOString(),
            sentiment: 'Netral. Data baru diinisialisasi. Berikan waktu untuk memproses ulasan Google Maps Anda.',
            top_positive_reviews: ['"Toko baru yang menjanjikan!"'],
            top_negative_reviews: ['"Belum banyak ulasan."'],
            strengths: ['Brand baru yang fleksibel', 'Lokasi berkembang'],
            weaknesses: ['Belum dikenal pasar luas', 'Keterbatasan modal awal'],
            opportunities: ['Mengembangkan pangsa pasar digital', 'Kemitraan lokal'],
            threats: ['Kompetitor mapan di sekitarnya']
          }
        ]
      };

      activeBusiness.value = newBiz;

      // Populate mock competitors dynamically based on the new location
      competitors.value = [
        {
          id: 'comp_new_01',
          business_id: newBiz.id,
          owner_uid: 'user_default',
          name: 'Pesaing Lokal Utama',
          industry: industry,
          google_maps_rating: 4.4,
          google_maps_number_of_reviews: 150,
          google_maps_url: 'https://maps.google.com',
          competitor_type: CompetitorType.DIRECT,
          analysis_date: new Date().toISOString(),
          location: {
            address: 'Jl. Raya Dekat ' + name,
            subdistrict: newBiz.location.subdistrict,
            city: newBiz.location.city,
            state: newBiz.location.state,
            country: newBiz.location.country,
            latitude: newBiz.location.latitude + 0.0015,
            longitude: newBiz.location.longitude - 0.001
          },
          competitor_analysis: [
            {
              analysis_date: new Date().toISOString(),
              sentiment: 'Positif. Memiliki basis pelanggan lokal yang cukup setia.',
              top_positive_reviews: ['"Nyaman dan harga bersahabat."'],
              top_negative_reviews: ['"Pelayanan kadang agak lambat."'],
              strengths: ['Sudah beroperasi lebih lama', 'Harga terjangkau'],
              weaknesses: ['Menu kurang variatif'],
              opportunities: ['Layanan delivery'],
              threats: ['Kopi Nusantara yang baru dibuka']
            }
          ]
        }
      ];

      return newBiz;
    } catch (err: any) {
      error.value = err.message || 'Gagal membuat bisnis.';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function updateBusiness(payload: Partial<Business>) {
    loading.value = true;
    error.value = null;
    try {
      await new Promise(resolve => setTimeout(resolve, 500));
      if (!activeBusiness.value) throw new Error('Tidak ada bisnis aktif untuk diperbarui.');
      
      activeBusiness.value = {
        ...activeBusiness.value,
        ...payload
      };
      return activeBusiness.value;
    } catch (err: any) {
      error.value = err.message || 'Gagal memperbarui bisnis.';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function deleteBusiness() {
    loading.value = true;
    error.value = null;
    try {
      await new Promise(resolve => setTimeout(resolve, 600));
      activeBusiness.value = null;
      competitors.value = [];
    } catch (err: any) {
      error.value = err.message || 'Gagal menghapus bisnis.';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  return {
    activeBusiness,
    competitors,
    loading,
    error,
    loadDemoData,
    createBusiness,
    updateBusiness,
    deleteBusiness
  };
});
