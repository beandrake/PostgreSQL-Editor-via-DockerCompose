import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
	  //forward any requests with URL starting with /api to Flask backend URL
      '/api': 'http://backend:5000', 
    },
  },
})
