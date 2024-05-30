<script setup lang="ts">
import { RouterView } from 'vue-router';
</script>

<template>
  <div id="app">
    <RouterView class="full" />
  </div>
</template>
<style>
#app {
  display: flex; /* 使用flex布局确保子元素可以填满容器 */
  flex-direction: column; /* 子元素垂直排列 */
  height: 100vh;
  width: 100vw;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.full {
  height: 100%;
  width: 100%;
}
</style>
