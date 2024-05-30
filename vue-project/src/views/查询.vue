<template>
  <div class="flex gap-4 mb-4">
    <span>请输入股票代码 </span>
    <el-input v-model="input" style="width: 240px" placeholder="Please input" />
  </div>
  <el-table :data="tableData" :default-sort="{ prop: 'date', order: 'descending' }" style="width: 100%">
    <el-table-column prop="date" label="Date" sortable width="180" />
    <el-table-column prop="name" label="Name" width="180" />
    <el-table-column prop="address" label="Address" :formatter="formatter" />
  </el-table>
  <div class="example-pagination-block">
    <el-pagination layout="prev, pager, next" :total="1000" />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
const input = ref('');
import type { TableColumnCtx } from 'element-plus';

interface User {
  date: string;
  name: string;
  address: string;
}

const formatter = (row: User, column: TableColumnCtx<User>) => {
  return row.address;
};

const tableData: User[] = [
  {
    date: '2016-05-03',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-02',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-04',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-01',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
];
</script>
<style>
.example-pagination-block + .example-pagination-block {
  margin-top: 10px;
}
.example-pagination-block {
  margin-bottom: 16px;
}
</style>
