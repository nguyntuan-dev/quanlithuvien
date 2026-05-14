/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Be Vietnam Pro', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      colors: {
        primary: { DEFAULT: '#1a56db', hover: '#1e429f', light: '#ebf5ff' },
        success: { DEFAULT: '#057a55', light: '#f3faf7' },
        danger:  { DEFAULT: '#c81e1e', light: '#fdf2f2' },
        warning: { DEFAULT: '#b45309', light: '#fffbeb' },
        surface: { DEFAULT: '#ffffff', soft: '#f9fafb', muted: '#f3f4f6' },
        border:  { DEFAULT: '#e5e7eb', dark: '#d1d5db' },
        ink:     { DEFAULT: '#111827', muted: '#6b7280', faint: '#9ca3af' },
      },
      boxShadow: {
        card: '0 1px 3px rgba(0,0,0,.07), 0 1px 2px rgba(0,0,0,.04)',
        dialog: '0 20px 60px rgba(0,0,0,.18)',
      }
    },
  },
  plugins: [],
}
