<template>
  <el-container style="width: 100%">
    <el-header style="padding: 0; height: 40px" class="underline-row">
      <el-row :gutter="0" style="height: 40px">
        <el-col :span="24" style="border-right: 1px solid gainsboro; border-radius: 0; display: flex; justify-content: center; align-items: center">代码详情</el-col>
      </el-row>
    </el-header>
    <el-main style="padding: 0; height: 100vh">
      <el-row :gutter="0" style="height: 100vh">
        <el-col :span="24" style="border-right: 1px solid gainsboro; border-radius: 0; overflow: auto; align-items: flex-start; height: 100%">
          <div v-if="codeText" v-html="codeText" style="padding-left: 10px; height: calc(100vh - 100px); overflow-y: auto; white-space: pre-wrap; font-family: 'Courier New', monospace"></div>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
export default {
  setup() {
    const route = useRoute();
    const codeText = ref(null); // 初始化为 null

    onMounted(async () => {
      const strategy_name = route.params.name;
      await fetchStockDetails(strategy_name);
    });

    async function fetchStockDetails(name) {
      try {
        const response = await axios.post('http://127.0.0.1:5000/strategy', { name: name });
        let data = response.data.strategy;
        console.log('Strategy Data:', data); // 打印查看data的具体内容和类型

        if (Array.isArray(data) && data.length > 0) {
          // 如果data是数组且不为空，取第一个元素（假设只有一个字符串）
          data = data[0];
        }

        // 替换换行符为HTML的<br>标签
        if (typeof data === 'string') {
          data = data.replace(/\n/g, '<br>');
        }

        codeText.value = data;
      } catch (error) {
        console.error('Failed to fetch stock details:', error);
      }
    }

    return {
      codeText,
    };
  },
};
</script>

<style>
.underline-row {
  border-bottom: 1px solid gainsboro;
}
</style>
