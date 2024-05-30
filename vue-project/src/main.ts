import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

//导入element plus 
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'   //样式设置

const app = createApp(App)

app.use(ElementPlus)
app.use(router); // 启用 router

app.mount('#app')
