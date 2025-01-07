import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
  root: './src',
  build: {
    outDir: path.resolve(__dirname, 'dist'),
  },
  server: {
    open: true
  }
});