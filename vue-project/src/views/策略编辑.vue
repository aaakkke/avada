<template>
  <div>
    <h1>策略编辑</h1>
    <p>策略名称: {{ name }}</p>
  </div>
</template>

<script lang="ts" setup>
import { useRoute } from 'vue-router';

const route = useRoute();
const name = route.params.name;
</script>
