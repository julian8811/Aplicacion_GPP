/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        primary: {
          DEFAULT: "#004191",
          foreground: "#ffffff",
        },
        secondary: {
          DEFAULT: "#f7f9fb",
          foreground: "#0f172a",
        },
        accent: {
          DEFAULT: "#0058be",
          foreground: "#ffffff",
        },
        muted: {
          DEFAULT: "#f7f9fb",
          foreground: "#64748b",
        },
        success: "#059669",
        warning: "#d97706",
        error: "#be123c",
        border: "#e2e8f0",
        background: "#f7f9fb",
        foreground: "#0f172a",
      },
      borderRadius: {
        lg: "16px",
        md: "8px",
        sm: "4px",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      boxShadow: {
        ambient: "0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px 0 rgba(0, 0, 0, 0.03)",
        lift: "0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04)",
      },
    },
  },
  plugins: [],
}