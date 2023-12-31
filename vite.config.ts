import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { viteSingleFile } from "vite-plugin-singlefile"

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    // Proxy Setup for avoid CORS conflict due to llama.cpp serve
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8080/", // default server.cpp port
        changeOrigin: true,
        cors:false,
        secure: false,
        rewrite: (path) => path.replace("/api/", ""),
      },
    },
  },
  plugins: [vue(), viteSingleFile()],
})
