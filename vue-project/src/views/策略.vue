<template>
  <el-text class="mx-1" type="primary" size="large">推荐策略</el-text>
  <el-table :data="tableData.slice(0, 1)" stripe style="width: 100%">
    <el-table-column type="index" width="50" />
    <el-table-column prop="name" label="策略名称" width="180" />
    <el-table-column label="属性" width="300">
      <template #default="scope">
        <div>
          <el-tag v-for="(attr, index) in scope.row.attribute" :key="index" :type="attr === '高风险' ? 'danger' : 'success'" class="mx-1">{{ attr }}</el-tag>
        </div>
      </template>
    </el-table-column>
    <el-table-column label="操作" width="240">
      <template #default="scope">
        <el-button type="primary" size="small" plain :icon="Edit" @click="editItem(scope.row)">编辑</el-button>
        <el-button v-if="scope.row.state" type="primary" size="small" plain :icon="CircleClose" @click="toggleSelect(scope.row)">取消选用</el-button>
        <el-button v-else type="primary" size="small" plain :icon="CircleCheck" @click="toggleSelect(scope.row)">选用</el-button>
      </template>
    </el-table-column>
    <el-table-column prop="state" label="状态">
      <template #default="scope">
        <el-tag :type="scope.row.state ? 'success' : 'info'">
          {{ scope.row.state ? '选用' : '未选用' }}
        </el-tag>
      </template>
    </el-table-column>
  </el-table>
  <el-text class="mx-1" type="primary" size="large">其他策略</el-text>
  <el-table :data="tableData.slice(1)" stripe style="width: 100%">
    <el-table-column type="index" width="50" />
    <el-table-column prop="name" label="策略名称" width="180" />
    <el-table-column label="属性" width="300">
      <template #default="scope">
        <div>
          <el-tag v-for="(attr, index) in scope.row.attribute" :key="index" :type="attr === '高风险' ? 'danger' : 'success'" class="mx-1">{{ attr }}</el-tag>
        </div>
      </template>
    </el-table-column>
    <el-table-column label="操作" width="240">
      <template #default="scope">
        <el-button type="primary" size="small" plain :icon="Edit" @click="editItem(scope.row)">编辑</el-button>
        <el-button v-if="scope.row.state" type="primary" size="small" plain :icon="CircleClose" @click="toggleSelect(scope.row)">取消选用</el-button>
        <el-button v-else type="primary" size="small" plain :icon="CircleCheck" @click="toggleSelect(scope.row)">选用</el-button>
      </template>
    </el-table-column>
    <el-table-column prop="state" label="状态">
      <template #default="scope">
        <el-tag :type="scope.row.state ? 'success' : 'info'">
          {{ scope.row.state ? '选用' : '未选用' }}
        </el-tag>
      </template>
    </el-table-column>
  </el-table>
</template>

<script lang="ts" setup>
import { Edit, CircleCheck, CircleClose } from '@element-plus/icons-vue';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter();
const tableData = ref([
  {
    name: '策略1',
    attribute: ['高风险', '高回报'],
    state: true,
  },
  {
    name: '策略1',
    attribute: ['高风险', '高回报'],
    state: true,
  },
  {
    name: '策略1',
    attribute: ['高风险', '高回报'],
    state: false,
  },
  {
    name: '策略1',
    attribute: ['高风险', '高回报'],
    state: true,
  },
  {
    name: '策略1',
    attribute: ['低风险', '中回报'],
    state: false,
  },
  {
    name: '策略1',
    attribute: ['中风险', '低回报'],
    state: false,
  },
]);

const editItem = (row: any) => {
  router.push({ name: '编辑', params: { name: row.name } });
};

const toggleSelect = (row: any) => {
  row.state = !row.state;
};
</script>

<style lang="scss">
.mx-1 {
  margin-left: 5px;
  margin-right: 5px;
}
</style>
