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
    {
      pattern: /bg-(red|green|blue|amber)-(100|200|300|800)/, // Includes bg of all colors and shades
    },
    {
      pattern: /text-(red|green|blue|amber)-(100|700|800)/, // Includes bg of all colors and shades
    },
    {
      pattern: /border-(red|green|blue|amber)-(700)/, // Includes bg of all colors and shades
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
        '2xs': '0.66rem',
      },
      maxWidth: {
        '8xl': '88rem',
        '9xl': '96rem',
        '10xl': '104rem',
      },
      blur: {
        xs: '2px',
      }
    },
  },
  plugins: [
  ],
  darkMode: ['selector'],
}
