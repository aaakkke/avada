<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <div id="app">
      <div class="nav">
          <RouterLink to="/查询">查询</RouterLink>
          <RouterLink to="/策略">策略</RouterLink>
          <RouterLink to="/交易">交易</RouterLink>
          <RouterLink to="/设置">设置</RouterLink>
      </div>
      <router-view/>
    </div>
</template>

