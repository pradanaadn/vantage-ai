<script setup lang="ts">
import { 
  TrendingUp, 
  Target, 
  Globe, 
  Sparkles,
  Search,
  CheckCircle,
  Clock
} from 'lucide-vue-next';
import BaseButton from '../components/base/BaseButton.vue';
import BaseCard from '../components/base/BaseCard.vue';
import copy from '../assets/copy.json';
import VantageLogo from '../components/base/VantageLogo.vue';

const content = copy.landing;
const branding = copy.auth.branding;

const iconMap: Record<string, any> = {
  TrendingUp,
  Target,
  Globe
};
</script>

<template>
  <div class="min-h-screen bg-slate-50 text-slate-800 font-sans overflow-x-hidden selection:bg-emerald-100 selection:text-emerald-900">
    <!-- Custom CSS Dotted Grid Backdrop overlay -->
    <div class="absolute inset-0 bg-dotted-pattern pointer-events-none opacity-[0.4] z-0"></div>

    <!-- Navigation -->
    <nav class="fixed top-0 z-50 w-full px-6 md:px-12 h-20 flex items-center justify-between backdrop-blur-md bg-white/80 border-b border-slate-200/60 shadow-sm">
      <div class="flex items-center gap-3">
        <VantageLogo class-name="w-10 h-10 hover:scale-105 transition-transform duration-300" />
        <span class="text-xl font-black tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-emerald-600 to-teal-700 uppercase">{{ branding.name }}</span>
      </div>

      <div class="hidden md:flex items-center gap-10">
        <a href="#solutions" class="text-sm font-extrabold uppercase tracking-wider text-slate-500 hover:text-emerald-600 transition-colors">Solutions</a>
        <a href="#preview" class="text-sm font-extrabold uppercase tracking-wider text-slate-500 hover:text-emerald-600 transition-colors">Dashboard Preview</a>
        <a href="#mission" class="text-sm font-extrabold uppercase tracking-wider text-slate-500 hover:text-emerald-600 transition-colors">Our Mission</a>
      </div>

      <div class="flex items-center gap-6">
        <router-link to="/login" class="text-sm font-extrabold uppercase tracking-wider text-slate-500 hover:text-emerald-600 transition-colors">Login</router-link>
        <router-link to="/signup">
          <BaseButton variant="primary" size="sm">Get Started</BaseButton>
        </router-link>
      </div>
    </nav>

    <!-- Hero Section: Custom Asymmetrical Layout -->
    <section class="relative min-h-screen pt-32 pb-20 px-6 md:px-12 flex flex-col justify-center items-center z-10 max-w-7xl mx-auto">
      
      <!-- Premium Multi-Stop Gradient Bands (Custom shapes instead of generic blurry circles) -->
      <div class="absolute inset-0 z-0 pointer-events-none overflow-hidden">
        <div class="absolute -top-40 right-10 w-[700px] h-[500px] bg-gradient-to-br from-emerald-200/50 via-teal-100/30 to-amber-100/20 blur-[130px] rounded-full transform rotate-12"></div>
        <div class="absolute -bottom-40 -left-20 w-[600px] h-[600px] bg-gradient-to-tr from-mint-200/20 via-emerald-100/40 to-transparent blur-[150px] rounded-full"></div>
      </div>

      <div class="w-full grid grid-cols-1 lg:grid-cols-12 gap-12 items-center relative z-10">
        
        <!-- Left Side: Dynamic Copy & Offset Accent Elements -->
        <div class="lg:col-span-7 space-y-8 text-left">
          
          <!-- Bespoke badge -->
          <div class="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-emerald-50 border border-emerald-200/60 text-emerald-700 text-xs font-black uppercase tracking-wider shadow-sm hover:scale-[1.02] transition-transform">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            {{ content.hero.badge }}
          </div>

          <!-- Bold, non-monotone typography -->
          <h1 class="text-5xl md:text-[68px] lg:text-[76px] font-black leading-[0.9] tracking-tighter text-slate-900">
            Grow Your Business<br/>
            <span class="bg-clip-text text-transparent bg-gradient-to-r from-emerald-600 via-emerald-500 to-teal-600">With Absolute Confidence</span>
          </h1>

          <p class="text-lg md:text-xl text-slate-600 font-medium leading-relaxed max-w-xl">
            {{ content.hero.subtitle }}
          </p>

          <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-4 pt-2">
            <router-link to="/signup" class="sm:flex-none">
              <BaseButton variant="primary" size="md" class="w-full px-10 shadow-lg shadow-emerald-500/20 hover:shadow-emerald-500/30">Start Free Journey</BaseButton>
            </router-link>
            <a href="#preview" class="sm:flex-none">
              <BaseButton variant="secondary" size="md" class="w-full px-8 hover:border-slate-300">Explore Demo</BaseButton>
            </a>
          </div>

          <!-- Trust Badges with offset alignments -->
          <div class="pt-8 border-t border-slate-200/60 max-w-lg grid grid-cols-3 gap-6 text-left">
            <div v-for="stat in content.stats" :key="stat.label" class="space-y-1">
              <p class="text-3xl font-black text-slate-950 flex items-center gap-1">
                {{ stat.value }}
                <span class="text-emerald-500 text-lg">+</span>
              </p>
              <p class="text-[11px] font-extrabold uppercase tracking-wider text-slate-400 leading-none">{{ stat.label }}</p>
            </div>
          </div>

        </div>

        <!-- Right Side: Bespoke Overlapping Card Grid (Breaks the typical mockup/AI mold) -->
        <div class="lg:col-span-5 relative flex justify-center items-center py-8">
          
          <!-- Decorative geometric frame -->
          <div class="absolute -inset-2 bg-gradient-to-tr from-emerald-100 to-teal-50 rounded-[40px] transform -rotate-2 -z-10 shadow-sm border border-emerald-200/30"></div>
          
          <!-- Bespoke Asymmetrical Grid layout -->
          <div class="w-full space-y-6">
            
            <!-- Card 1: Profit Guard -->
            <div class="bg-white border border-slate-200 p-6 rounded-3xl shadow-md relative hover:-translate-y-1 transition-transform duration-300 transform -rotate-1 hover:rotate-0">
              <div class="absolute -top-3 -right-3 bg-emerald-500 text-white p-1.5 rounded-xl shadow-md">
                <Sparkles class="w-4 h-4" />
              </div>
              <div class="flex gap-4 items-start">
                <div class="bg-emerald-50 p-3 rounded-2xl border border-emerald-100 text-emerald-600 shrink-0">
                  <TrendingUp class="w-6 h-6" />
                </div>
                <div>
                  <h3 class="text-lg font-black text-slate-900 mb-1">Profit Guard</h3>
                  <p class="text-xs text-slate-500 leading-relaxed font-semibold">Instantly optimize margins and detect leaks. Average cash flow boost: <strong>+14.2%</strong></p>
                </div>
              </div>
            </div>

            <!-- Card 2: Market Explorer with Offset -->
            <div class="bg-white border border-slate-200 p-6 rounded-3xl shadow-md relative hover:-translate-y-1 transition-transform duration-300 ml-6 transform rotate-1 hover:rotate-0 border-l-4 border-l-emerald-500">
              <div class="flex gap-4 items-start">
                <div class="bg-teal-50 p-3 rounded-2xl border border-teal-100 text-teal-600 shrink-0">
                  <Target class="w-6 h-6" />
                </div>
                <div>
                  <h3 class="text-lg font-black text-slate-900 mb-1">Market Explorer</h3>
                  <p class="text-xs text-slate-500 leading-relaxed font-semibold">Hyper-local gaps scanned automatically. <strong>18 high-demand fields</strong> spotted this week.</p>
                </div>
              </div>
            </div>

            <!-- Card 3: Future Forecast with Offset -->
            <div class="bg-white border border-slate-200 p-6 rounded-3xl shadow-md relative hover:-translate-y-1 transition-transform duration-300 mr-6 transform -rotate-1 hover:rotate-0">
              <div class="flex gap-4 items-start">
                <div class="bg-amber-50 p-3 rounded-2xl border border-amber-100 text-amber-600 shrink-0">
                  <Globe class="w-6 h-6" />
                </div>
                <div>
                  <h3 class="text-lg font-black text-slate-900 mb-1">Future Forecast</h3>
                  <p class="text-xs text-slate-500 leading-relaxed font-semibold">Track local macroeconomic & traffic patterns to unlock smart planning choices.</p>
                </div>
              </div>
            </div>

          </div>

        </div>

      </div>
    </section>

    <!-- Custom Bold Color Band: Makes the page exciting and visually spectacular -->
    <section id="solutions" class="relative py-24 bg-gradient-to-r from-emerald-950 via-teal-900 to-emerald-900 text-white overflow-hidden shadow-2xl">
      <!-- Blueprint Grid pattern overlay in the dark band -->
      <div class="absolute inset-0 bg-dotted-pattern pointer-events-none opacity-[0.08] z-0"></div>
      
      <div class="absolute inset-0 pointer-events-none overflow-hidden">
        <div class="absolute -right-20 top-0 w-[500px] h-[500px] bg-emerald-500/10 blur-[130px] rounded-full"></div>
        <div class="absolute -left-20 bottom-0 w-[400px] h-[400px] bg-teal-500/10 blur-[120px] rounded-full"></div>
      </div>

      <div class="max-w-7xl mx-auto px-6 md:px-12 relative z-10">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          
          <div class="lg:col-span-5 space-y-6">
            <span class="text-[10px] font-black tracking-widest text-emerald-400 bg-emerald-900/50 border border-emerald-800/80 px-3.5 py-1.5 rounded-full uppercase">Growth Suite Advantage</span>
            <h2 class="text-4xl md:text-5xl font-black tracking-tight leading-tight">
              Designed For Business Owners, Not Academics
            </h2>
            <p class="text-emerald-100/80 font-medium leading-relaxed">
              We understand you don't have time to stare at dry, generic charts. Vantage AI does the heavy lifting, synthesizing local and financial parameters to offer simple, action-oriented directives.
            </p>
            <div class="pt-2">
              <router-link to="/signup">
                <BaseButton variant="primary" class="!bg-white !text-emerald-950 hover:!bg-emerald-50 shadow-xl shadow-black/10">Claim Your Account</BaseButton>
              </router-link>
            </div>
          </div>

          <div class="lg:col-span-7 grid grid-cols-1 sm:grid-cols-3 gap-6">
            <div v-for="feature in content.features" :key="feature.id" class="bg-white/5 border border-white/10 p-6 rounded-3xl backdrop-blur-md hover:bg-white/10 transition-colors">
              <div class="bg-emerald-500/25 border border-emerald-500/30 p-3 rounded-2xl w-fit mb-4 text-emerald-300">
                <component :is="iconMap[feature.icon]" class="w-6 h-6" />
              </div>
              <h3 class="text-lg font-bold mb-2 text-white">{{ feature.title }}</h3>
              <p class="text-xs text-emerald-100/70 font-medium leading-relaxed">{{ feature.description }}</p>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- Interactive Mock Dashboard (Verifiably light and gorgeous) -->
    <section id="preview" class="py-24 px-6 md:px-12 bg-slate-50 relative z-10">
      <div class="max-w-7xl mx-auto space-y-12">
        <div class="text-center max-w-2xl mx-auto space-y-4">
          <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-emerald-50 border border-emerald-100 text-emerald-700 text-xs font-black uppercase tracking-wider shadow-sm">
            <Clock class="w-4 h-4 text-emerald-500" />
            Live Platform Simulation
          </div>
          <h2 class="text-4xl font-black tracking-tight text-slate-900">Your Simple Growth Blueprint</h2>
          <p class="text-slate-600 font-semibold">Everything you need to guide your store, agency, or local trade to a brighter, richer future.</p>
        </div>

        <!-- Custom Mock Window Frame -->
        <BaseCard class="border-slate-200/80 bg-white/95 backdrop-blur-md shadow-2xl max-w-5xl mx-auto !p-0 overflow-hidden relative border-t-8 border-t-emerald-600">
          
          <!-- Top Window Bar -->
          <div class="bg-slate-100/70 border-b border-slate-200/60 px-6 py-4 flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="w-3.5 h-3.5 rounded-full bg-rose-400"></span>
              <span class="w-3.5 h-3.5 rounded-full bg-amber-400"></span>
              <span class="w-3.5 h-3.5 rounded-full bg-emerald-400"></span>
              <span class="text-xs font-bold text-slate-400 ml-4 font-mono select-none">vantage-intelligence-dashboard.app</span>
            </div>
            <div>
              <span class="px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-black uppercase flex items-center gap-1.5 shadow-sm">
                <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                Growth Guard Scanner Active
              </span>
            </div>
          </div>

          <!-- Mock Dashboard Body -->
          <div class="p-6 bg-slate-50/40 grid grid-cols-1 lg:grid-cols-12 gap-6 z-10 relative">
            
            <!-- Left Side: Interactive Metrics & Asymmetric Chart -->
            <div class="lg:col-span-8 space-y-6">
              
              <!-- Mini metrics grid -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm relative overflow-hidden">
                  <div class="absolute top-0 right-0 bg-emerald-500/10 text-emerald-600 px-3 py-1 rounded-bl-xl text-[10px] font-black uppercase tracking-wider">Cash Flow</div>
                  <div class="flex items-center justify-between">
                    <span class="text-xs font-black uppercase tracking-wider text-slate-400">Monthly Surplus</span>
                    <TrendingUp class="w-5 h-5 text-emerald-500" />
                  </div>
                  <div class="flex items-baseline gap-2 mt-2">
                    <p class="text-3xl font-black text-slate-900">$45,280</p>
                    <span class="text-[11px] font-extrabold text-emerald-600 bg-emerald-50 border border-emerald-100/50 px-1.5 py-0.5 rounded-md">+14.2%</span>
                  </div>
                  <p class="text-xs font-semibold text-slate-400 mt-2">Optimized cash flow by Profit Guard</p>
                </div>

                <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm relative overflow-hidden">
                  <div class="absolute top-0 right-0 bg-teal-500/10 text-teal-600 px-3 py-1 rounded-bl-xl text-[10px] font-black uppercase tracking-wider">Demographics</div>
                  <div class="flex items-center justify-between">
                    <span class="text-xs font-black uppercase tracking-wider text-slate-400">Market Opportunities</span>
                    <Target class="w-5 h-5 text-teal-500" />
                  </div>
                  <div class="flex items-baseline gap-2 mt-2">
                    <p class="text-3xl font-black text-slate-900">18 Scans</p>
                    <span class="text-[11px] font-extrabold text-teal-600 bg-teal-50 border border-teal-100/50 px-1.5 py-0.5 rounded-md">Excellent</span>
                  </div>
                  <p class="text-xs font-semibold text-slate-400 mt-2">Hyper-local competitor gaps checked</p>
                </div>
              </div>

              <!-- Main Trajectory Chart (Asymmetrical UI detail) -->
              <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm space-y-4">
                <div class="flex items-center justify-between">
                  <div class="space-y-1">
                    <span class="text-xs font-black uppercase tracking-wider text-slate-400">Profit Trajectory</span>
                    <h4 class="font-extrabold text-slate-800">Quarterly Growth Trends</h4>
                  </div>
                  <div class="flex items-center gap-4 text-xs font-bold">
                    <span class="flex items-center gap-1.5 text-slate-400">
                      <span class="w-2 h-2 rounded-full bg-slate-200"></span> Prior Strategy
                    </span>
                    <span class="flex items-center gap-1.5 text-emerald-600">
                      <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span> Vantage Optimized
                    </span>
                  </div>
                </div>

                <!-- Custom non-generic chart -->
                <div class="h-44 flex items-end justify-between gap-4 pt-6 border-b border-slate-100 px-2">
                  <div class="w-full flex flex-col items-center gap-2">
                    <div class="w-full bg-emerald-50 hover:bg-emerald-100/80 transition-all rounded-t-xl h-16 relative group">
                      <div class="absolute -top-8 left-1/2 -translate-x-1/2 bg-slate-800 text-white text-[10px] font-bold px-2.5 py-1 rounded shadow-md opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">$12,400</div>
                    </div>
                    <span class="text-[10px] font-black text-slate-400 uppercase tracking-wider">May</span>
                  </div>
                  <div class="w-full flex flex-col items-center gap-2">
                    <div class="w-full bg-emerald-100 hover:bg-emerald-200/80 transition-all rounded-t-xl h-24 relative group">
                      <div class="absolute -top-8 left-1/2 -translate-x-1/2 bg-slate-800 text-white text-[10px] font-bold px-2.5 py-1 rounded shadow-md opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">$18,200</div>
                    </div>
                    <span class="text-[10px] font-black text-slate-400 uppercase tracking-wider">Jun</span>
                  </div>
                  <div class="w-full flex flex-col items-center gap-2">
                    <div class="w-full bg-emerald-200 hover:bg-emerald-300/80 transition-all rounded-t-xl h-28 relative group">
                      <div class="absolute -top-8 left-1/2 -translate-x-1/2 bg-slate-800 text-white text-[10px] font-bold px-2.5 py-1 rounded shadow-md opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">$22,800</div>
                    </div>
                    <span class="text-[10px] font-black text-slate-400 uppercase tracking-wider">Jul</span>
                  </div>
                  <div class="w-full flex flex-col items-center gap-2">
                    <div class="w-full bg-gradient-to-t from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 transition-all rounded-t-xl h-40 relative group shadow-md shadow-emerald-500/10">
                      <div class="absolute -top-8 left-1/2 -translate-x-1/2 bg-slate-900 text-white text-[10px] font-bold px-2.5 py-1 rounded shadow-md opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">$32,500</div>
                    </div>
                    <span class="text-[10px] font-black text-slate-400 uppercase tracking-wider">Aug</span>
                  </div>
                </div>
              </div>

            </div>

            <!-- Right Side: Smart Action Blueprint -->
            <div class="lg:col-span-4 bg-white p-5 rounded-2xl border border-slate-100 shadow-sm flex flex-col justify-between">
              <div>
                <div class="border-b border-slate-100 pb-3 flex items-center justify-between mb-4">
                  <h4 class="font-black text-slate-800 flex items-center gap-2 text-sm uppercase tracking-wide">
                    <Sparkles class="w-4 h-4 text-emerald-500" />
                    Growth Directives
                  </h4>
                  <span class="text-[9px] font-black uppercase text-slate-400 bg-slate-100 px-2 py-0.5 rounded">Scanned Aug</span>
                </div>

                <!-- Recommendation Stack -->
                <div class="space-y-4">
                  <div class="p-3 bg-emerald-50/50 hover:bg-emerald-50 border border-emerald-100/50 rounded-xl transition-all duration-300 flex gap-3 items-start group">
                    <div class="bg-emerald-100 p-2 rounded-lg text-emerald-600 shrink-0 group-hover:scale-105 transition-transform">
                      <Search class="w-4 h-4" />
                    </div>
                    <div class="space-y-0.5">
                      <p class="text-xs font-black text-slate-800">Uncovered Gap in Westside</p>
                      <p class="text-[10px] text-slate-500 font-semibold leading-relaxed">Market Explorer scanned high local interest for delivery hubs.</p>
                    </div>
                  </div>

                  <div class="p-3 bg-teal-50/50 hover:bg-teal-50 border border-teal-100/50 rounded-xl transition-all duration-300 flex gap-3 items-start group">
                    <div class="bg-teal-100 p-2 rounded-lg text-teal-600 shrink-0 group-hover:scale-105 transition-transform">
                      <CheckCircle class="w-4 h-4" />
                    </div>
                    <div class="space-y-0.5">
                      <p class="text-xs font-black text-slate-800">Marginal leaks plugged</p>
                      <p class="text-[10px] text-slate-500 font-semibold leading-relaxed">Profit Guard identified $340 overlap in active local utilities.</p>
                    </div>
                  </div>

                  <div class="p-3 bg-amber-50/50 hover:bg-amber-50 border border-amber-100/50 rounded-xl transition-all duration-300 flex gap-3 items-start group">
                    <div class="bg-amber-100 p-2 rounded-lg text-amber-600 shrink-0 group-hover:scale-105 transition-transform">
                      <Sparkles class="w-4 h-4" />
                    </div>
                    <div class="space-y-0.5">
                      <p class="text-xs font-black text-slate-800">Demand Bump Saturday</p>
                      <p class="text-[10px] text-slate-500 font-semibold leading-relaxed">Forecast predicts a 15% foot-traffic bump in local shopping area.</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Button link -->
              <router-link to="/signup" class="block pt-4">
                <BaseButton variant="outline" size="sm" class="w-full text-xs py-3 border-emerald-600 text-emerald-600 hover:bg-emerald-50">Explore Full Directives</BaseButton>
              </router-link>
            </div>

          </div>
        </BaseCard>
      </div>
    </section>

    <!-- Solid Mission CTA Area (Non-monoton, clean layouts) -->
    <section id="mission" class="relative py-24 px-6 md:px-12 bg-white relative z-10 border-t border-slate-200/60 overflow-hidden">
      <!-- Dotted grids backdrop for mission -->
      <div class="absolute inset-0 bg-dotted-pattern pointer-events-none opacity-[0.2] z-0"></div>

      <div class="max-w-4xl mx-auto text-center space-y-8 relative z-10">
        <span class="text-xs font-black tracking-widest text-emerald-600 bg-emerald-50 border border-emerald-100 px-3.5 py-1.5 rounded-full uppercase">Your Future Awaits</span>
        <h2 class="text-4xl md:text-5xl font-black text-slate-900 tracking-tight leading-tight">
          {{ content.ctaSection.title }}
        </h2>
        <p class="text-lg md:text-xl text-slate-600 font-medium max-w-2xl mx-auto">
          {{ content.ctaSection.subtitle }}
        </p>
        <div class="pt-4">
          <router-link to="/signup">
            <BaseButton variant="primary" size="lg" class="shadow-xl shadow-emerald-500/20">{{ content.ctaSection.button }}</BaseButton>
          </router-link>
        </div>
      </div>
    </section>

    <!-- Footer: Clean, modern light footer -->
    <footer class="py-16 px-6 md:px-12 border-t border-slate-200/60 bg-slate-50 relative z-10">
      <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-start gap-12">
        <div class="space-y-6">
          <div class="flex items-center gap-3">
            <VantageLogo class-name="w-11 h-11" />
            <span class="text-xl font-black tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-emerald-600 to-teal-700 uppercase">{{ branding.name }}</span>
          </div>
          <p class="text-slate-500 font-semibold max-w-xs text-sm">
            The next generation of SME intelligence. Built for growth, powered by trust.
          </p>
        </div>

        <div class="grid grid-cols-2 gap-12 md:gap-24">
          <div class="space-y-4">
            <h4 class="text-xs font-black uppercase tracking-wider text-emerald-600">Pillars</h4>
            <ul class="space-y-2 text-slate-500 text-sm font-bold">
              <li><a href="#" class="hover:text-emerald-600 transition-colors">Profit Guard</a></li>
              <li><a href="#" class="hover:text-emerald-600 transition-colors">Market Explorer</a></li>
              <li><a href="#" class="hover:text-emerald-600 transition-colors">Future Forecast</a></li>
            </ul>
          </div>
          <div class="space-y-4">
            <h4 class="text-xs font-black uppercase tracking-wider text-emerald-600">Company</h4>
            <ul class="space-y-2 text-slate-500 text-sm font-bold">
              <li><a href="#" class="hover:text-emerald-600 transition-colors">Privacy Policy</a></li>
              <li><a href="#" class="hover:text-emerald-600 transition-colors">Security Standards</a></li>
              <li><a href="#" class="hover:text-emerald-600 transition-colors">Terms of Service</a></li>
            </ul>
          </div>
        </div>
      </div>
      <div class="max-w-7xl mx-auto mt-16 pt-8 border-t border-slate-200/60 text-center">
        <p class="text-[11px] font-black tracking-wider text-slate-400 uppercase">© 2026 Vantage AI Growth Systems. Helping local business thrive.</p>
      </div>
    </footer>
  </div>
</template>

<style>
/* Blueprint Dotted Layout background */
.bg-dotted-pattern {
  background-image: radial-gradient(#cbd5e1 1.2px, transparent 1.2px);
  background-size: 24px 24px;
}
</style>
