<template>
  <div class="flex gap-4 mb-4">
    <div style="height: 10px"></div>
    <span>请输入股票代码 </span>
    <el-input v-model="input" style="width: 240px" placeholder="Please input">
      <template #append>
        <el-button :icon="Search" @click="fetchStockData"></el-button>
      </template>
    </el-input>
  </div>
  <div>
    <el-table v-loading="loading" :data="paginatedData" :default-sort="{ prop: '股票代码', order: 'descending' }" style="width: 100%" height="380">
      <el-table-column fixed type="index" width="50" />
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
        <template v-slot:default="scope: { row: Stock }">
          <el-button link type="primary" size="small" @click="handleDetailClick(scope.row.股票代码)"> 详情 </el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="example-pagination-block" v-if="!input || input.length === 0">
      <el-pagination @current-change="handleCurrentChange" :current-page="currentPage" :page-size="pageSize" :total="totalItems" layout="prev, pager, next" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, onUnmounted } from 'vue';
import { Search } from '@element-plus/icons-vue';
import axios from 'axios';
import { useRouter, useRoute } from 'vue-router'; // 引入useRouter
import { ElLoading } from 'element-plus'; // 引入 ElLoading

const loading = ref(false); // 添加 loading 状态
const input = ref('');
const tableData = ref([]);
const currentPage = ref(1);
const pageSize = ref(30);
const totalItems = ref(0);
const refreshInterval = ref<ReturnType<typeof setInterval> | null>(null);
const router = useRouter(); // 使用useRouter
const route = useRoute(); // 获取路由实例

const boardType = computed(() => route.query.board); // 从查询参数中获取板块类型

interface Stock {
  股票代码: string;
  名称: string;
  最新价: string;
  涨跌额: string;
  涨跌幅: string;
  成交量: string;
  成交额: string;
  昨收: string;
  今开: string;
  振幅: string;
  最高价: string;
  最低价: string;
  量比: string;
  换手率: string;
}
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return tableData.value.slice(start, end);
});

const handleDetailClick = (code) => {
  router.push(`/index/stock/${code}`);
};

const handleCurrentChange = (newPage) => {
  currentPage.value = newPage;
  fetchStockData();
};

onMounted(() => {
  fetchStockData();
  refreshInterval.value = setInterval(fetchStockData, 10000);
});

const fetchStockData = async () => {
  const type1 = boardType.value;
  loading.value = true; // 显示加载效果
  try {
    if (input.value) {
      //股票查询
      const response = await axios.post('http://127.0.0.1:5000/stock_select', { code: input.value, type: type1 });
      console.log(response.data);
      tableData.value = response.data.stock_select;
      totalItems.value = response.data.stock_select.length;
      loading.value = false; // 隐藏加载效果
    } else {
      //显示所有股票信息
      const response = await axios.post('http://127.0.0.1:5000/stock', { type: type1 });
      tableData.value = response.data.stock;
      totalItems.value = response.data.stock.length;
      loading.value = false; // 隐藏加载效果
    }
  } catch (error) {
    console.error('获取股票数据时发生错误：', error);
  }
};
onUnmounted(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value);
  }
});
onUnmounted(() => {
  if (loading.value) {
    loading.value = false;
  }
});
</script>

<style>
.example-pagination-block + .example-pagination-block {
  margin-top: 10px;
}
.example-pagination-block {
  margin-bottom: 16px;
}
</style>
