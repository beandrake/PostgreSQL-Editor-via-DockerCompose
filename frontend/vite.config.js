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

	host: true, // allows dev server to be accessed from outside container
	port: 5173, // sets a consistent dev port (must match exposed port)
	strictPort: true, // don't use a different port if 5173 is unavailable
  },
})
