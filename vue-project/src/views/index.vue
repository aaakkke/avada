<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <el-row :gutter="20" background-color: aquamarine>
          <el-col :span="6"
            ><div class="grid-content ep-bg-purple" />
            Avada量化交易平台</el-col
          >
          <el-col :span="6" :offset="12">
            <div class="grid-content ep-bg-purple" />
            exit
          </el-col>
        </el-row>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <el-col>
            <el-menu default-active="2" class="el-menu-vertical-demo">
              <el-sub-menu index="1">
                <template #title>
                  <el-icon><Search /></el-icon>
                  <span>查询</span>
                </template>
                <el-menu-item index="1-1" router-link to="/沪市主板">沪市主板</el-menu-item>
                <el-menu-item index="1-2">深市主板</el-menu-item>
                <el-menu-item index="1-3">科创板</el-menu-item>
                <el-menu-item index="1-4">创业板</el-menu-item>
              </el-sub-menu>
              <el-menu-item index="2">
                <el-icon><Document /></el-icon>
                <span>策略</span>
              </el-menu-item>
              <el-menu-item index="3">
                <el-icon><Coin /></el-icon>
                <span>交易</span>
              </el-menu-item>
              <el-menu-item index="4">
                <el-icon><setting /></el-icon>
                <span>设置</span>
              </el-menu-item>
            </el-menu>
          </el-col>
        </el-aside>
        <el-main
          >Main
          <RouterView />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>
<script lang="ts" setup>
import { Document, Search, Coin, Setting } from '@element-plus/icons-vue';
</script>
<style lang="scss">
.common-layout {
  display: flex; /* 使用flex布局确保子元素可以填满容器 */
  flex-direction: column; /* 子元素垂直排列 */
  height: 100%; /* 高度占满父元素 */
  width: 100%; /* 宽度占满父元素 */
}
.el-row {
  margin-bottom: 20px;
}
.el-row:last-child {
  margin-bottom: 0;
}
.el-col {
  border-radius: 4px;
}
.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
.el-aside {
  display: flex; /* 使用flex布局确保子元素可以填满容器 */
}
.el-menu-vertical-demo {
  width: 100%;
}
</style>
