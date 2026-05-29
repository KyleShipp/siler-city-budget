/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        chatham: {
          blue: '#1b4d7a',
          gold: '#c9a227',
          dark: '#0f2e4a',
        },
      },
    },
  },
  plugins: [],
}
