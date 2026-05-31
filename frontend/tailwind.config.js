import daisyui from "daisyui"

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'Plus Jakarta Sans', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      colors: {
        vantage: {
          black: '#f8fafc', // Soft, clean off-white background
          dark: '#ffffff',  // Crisp white card and panel background
          glow: '#10b981',  // Warm emerald/mint glow
          accent: '#059669', // Growth emerald primary
          emerald: {
            400: '#34d399',
            500: '#10b981',
            600: '#059669',
          },
          slate: '#475569', // Clear, readable text slate gray
        }
      },
      animation: {
        'glow-pulse': 'glow-pulse 6s infinite ease-in-out',
      },
      keyframes: {
        'glow-pulse': {
          '0%, 100%': { opacity: 0.2, transform: 'scale(1)' },
          '50%': { opacity: 0.4, transform: 'scale(1.08)' },
        }
      }
    },
  },
  plugins: [daisyui],
  daisyui: {
    themes: ["corporate"], // Support corporate light theme only
    darkTheme: "corporate", // Prevent automatic dark-mode switching
  },
}

