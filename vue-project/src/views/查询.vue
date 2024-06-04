<template>
  <div class="flex gap-4 mb-4">
    <span>请输入股票代码 </span>
    <el-input v-model="input" style="width: 240px" placeholder="Please input">
      <template #append>
        <el-button :icon="Search" @click="fetchStockData"></el-button>
      </template>
    </el-input>
  </div>
  <div>
    <el-table :data="paginatedData" :default-sort="{ prop: '股票代码', order: 'descending' }" style="width: 100%" height="380">
      <el-table-column fixed prop="股票代码" label="代码" sortable width="100" />
      <el-table-column prop="名称" label="名称" width="180" />
      <el-table-column prop="最新价" label="最新价" width="180" />
      <el-table-column prop="涨跌幅" label="涨跌幅" width="180" />
      <el-table-column prop="涨跌额" label="涨跌额" width="180" />
      <el-table-column prop="成交量" label="成交量" width="180" />
      <el-table-column prop="成交额" label="成交额" width="180" />
      <el-table-column prop="振幅" label="振幅" width="180" />
      <el-table-column prop="最高价" label="最高" width="180" />
      <el-table-column prop="最低价" label="最低" width="180" />
      <el-table-column prop="今开" label="今开" width="180" />
      <el-table-column prop="昨收" label="昨收" width="180" />
      <el-table-column prop="量比" label="量比" width="180" />
      <el-table-column prop="换手率" label="换手率" width="180" />
      <el-table-column fixed="right" label="更多信息" width="120">
        <template #default>
          <el-button link type="primary" size="small" @click="handleClick"> 详情 </el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="example-pagination-block" v-if="!input || input.length === 0">
      <el-pagination @current-change="handleCurrentChange" :current-page="currentPage" :page-size="pageSize" :total="totalItems" layout="prev, pager, next" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue';
import { Search } from '@element-plus/icons-vue';
import axios from 'axios';

const input = ref('');
const tableData = ref([]);
const currentPage = ref(1);
const pageSize = ref(30);
const totalItems = ref(0);

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return tableData.value.slice(start, end);
});

const handleCurrentChange = (newPage) => {
  currentPage.value = newPage;
  fetchStockData();
};
const handleClick = () => {
  console.log('click');
};

onMounted(() => {
  fetchStockData();
});

const fetchStockData = async () => {
  try {
    if (input.value) {
      //股票查询
      const response = await axios.post('http://127.0.0.1:5000/stock_select', { code: input.value, type: 'sh' });
      console.log(response.data);
      tableData.value = response.data.stock;
      totalItems.value = response.data.stock.length;
    } else {
      //显示所有股票信息
      const response = await axios.post('http://127.0.0.1:5000/stock', { type: 'sh' });
      tableData.value = response.data.stock;
      totalItems.value = response.data.stock.length;
    }
  } catch (error) {
    console.error('获取股票数据时发生错误：', error);
  }
};
</script>
<style>
.example-pagination-block + .example-pagination-block {
  margin-top: 10px;
}
.example-pagination-block {
  margin-bottom: 16px;
}
</style>
