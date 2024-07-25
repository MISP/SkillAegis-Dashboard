/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  safelist: [
    {
      pattern: /bg-blue+/, // Includes bg of all colors and shades
    },
  ],
  theme: {
    extend: {
      transitionProperty: {
        'width': 'width'
      },
      screens: {
        '3xl': '1800px',
      },
      fontSize: {
        'xxs': '0.6rem',
      },
    },
  },
  plugins: [
  ],
  darkMode: ['selector'],
}
