<script setup lang="ts">   /* ts表示typesript*/
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const activeTab = ref('query')
interface TabInfo {
  props: {
    name: string;
  };
}
function handleTabClick(tab: TabInfo) {
  router.push({ name: tab.props.name });
}
</script>

<template>
  <el-container>
    <el-header>
      <el-tabs  v-model="activeTab" @tab-click="handleTabClick">
        <el-tab-pane label="查询" name="查询"></el-tab-pane>
        <el-tab-pane label="策略" name="策略"></el-tab-pane>
        <el-tab-pane label="交易" name="交易"></el-tab-pane>
        <el-tab-pane label="设置" name="设置"></el-tab-pane>
      </el-tabs>
    </el-header>
    <el-main>
      <router-view/>
    </el-main>
  </el-container>
</template>

<style scoped>
.el-main {
  position: relative;
  top: -50px;  /* 根据实际需要调整此值 */
}
</style>

