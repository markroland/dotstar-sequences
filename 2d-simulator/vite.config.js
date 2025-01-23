import { defineConfig } from 'vite';
import path from 'path';
import copy from 'rollup-plugin-copy';

export default defineConfig({
  root: './src',
  base: '',
  build: {
    outDir: '../dist',
    assetsDir: 'assets',
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, 'src/index.html'),
      },
      plugins: [
        copy({
          targets: [
            { src: 'src/*.png', dest: './dist' },
            { src: 'src/*.glsl', dest: './dist' },
            { src: 'src/*.css', dest: './dist' },
          ],
          hook: 'writeBundle',
        }),
      ],
    },
  },
  server: {
    open: true
  }
});