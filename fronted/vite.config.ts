import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    // Proxy Setup for avoid CORS conflict due to llama.cpp serve
    proxy: {
      "/api": {
        target: "http://127.0.0.1:5000/",
        changeOrigin: true,
        cors:false,
        secure: false,
        rewrite: (path) => path.replace("/api/", ""),
      },
    },
  },
  plugins: [vue()],
})
