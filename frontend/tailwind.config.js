/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // nb: tailwind can only look under root dir
    "./index.html",
    "./src/flask_blueprints/**/*.html.j2",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
