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
    require('daisyui'),
  ],
  darkMode: ['selector'],
  daisyui: {
    themes: false, // false: only light + dark | true: all themes | array: specific themes like this ["light", "dark", "cupcake"]
    darkTheme: "dark", // name of one of the included themes for dark mode
    base: false, // applies background color and foreground color for root element by default
    styled: true, // include daisyUI colors and design decisions for all components
    utils: false, // adds responsive and modifier utility classes
    prefix: "", // prefix for daisyUI classnames (components, modifiers and responsive class names. Not colors)
    logs: false, // Shows info about daisyUI version and used config in the console when building your CSS
    themeRoot: ":root", // The element that receives theme color CSS variables
  },
}
