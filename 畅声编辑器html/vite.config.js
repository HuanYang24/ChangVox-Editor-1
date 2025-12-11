import { defineConfig } from 'vite'

// https://vitejs.dev/config/
export default defineConfig({
  // 设置项目根目录
  root: '.',
  
  // 设置构建输出目录
  build: {
    outDir: 'dist',
    // 资产输出目录
    assetsDir: 'assets',
    // 最小化选项
    minify: 'esbuild',
    // 源映射
    sourcemap: true,
    // 构建后清空输出目录
    emptyOutDir: true,
    rollupOptions: {
      // 确保入口文件正确
      input: {
        main: './index.html'
      }
    }
  },
  
  // 开发服务器配置
  server: {
    // 端口号
    port: 3000,
    // 自动打开浏览器
    open: true,
    // 允许来自任何主机的请求
    host: true,
    // 代理配置（如果需要）
    proxy: {
      // 可以在这里配置代理，连接到C++后端服务
      // '/api': {
      //   target: 'http://localhost:8080',
      //   changeOrigin: true
      // }
    }
  },
  
  // 预览服务器配置
  preview: {
    port: 8080
  }
})