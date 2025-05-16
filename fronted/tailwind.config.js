/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}", // Asegura que Tailwind escanee todos los archivos relevantes en src
    "./public/index.html", // También puede ser útil escanear el index.html si usas clases de Tailwind allí
  ],
  theme: {
    extend: {
      // Aquí puedes extender el tema de Tailwind según tus necesidades.
      // Por ejemplo, añadir colores personalizados, fuentes, breakpoints, etc.
      fontFamily: {
        inter: ['Inter', 'sans-serif'], // Define la fuente Inter para usarla con class="font-inter"
      },
      colors: {

        'tpms-blue': '#007bff',
        'tpms-gray': {
          light: '#f8f9fa',
          DEFAULT: '#6c757d',
          dark: '#343a40',
        },
      },
    },
  },
  plugins: [

  ],
}
