<template>
  <div>
    <div style="height: 10px"></div>
    <div style="display: flex; align-items: center; margin-left: 5px">
      <el-button @click="goBack" type="primary" plain>返回</el-button>
      <h1 style="margin-left: 20px">股票详情</h1>
    </div>
    <div style="height: calc(100vh - 70px); overflow-y: auto">
      <canvas id="volumeChart" style="height: 100vh"></canvas>
      <canvas id="turnoverChart" style="height: 100vh"></canvas>
      <canvas id="highPriceChart" style="height: 100vh"></canvas>
      <canvas id="lowPriceChart" style="height: 100vh"></canvas>
      <canvas id="openPriceChart" style="height: 100vh"></canvas>
      <canvas id="closePriceChart" style="height: 100vh"></canvas>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import Chart from 'chart.js/auto';

// 使用useRoute来获取路由信息
const route = useRoute();
const router = useRouter();
const stockData = ref([]);

onMounted(async () => {
  const stockCode = route.params.code; // 获取股票代码
  await fetchStockDetails(stockCode);
});

// 定义获取股票详细信息的函数
async function fetchStockDetails(code1) {
  try {
    //股票历史信息获取
    const response = await axios.post('http://127.0.0.1:5000/stock_paint', { code: code1 });
    console.log(response.data);
    stockData.value = response.data.stock_paint; // 假设后端返回的数据直接是股票的详细信息
    await nextTick(); // 确保 DOM 更新
    createCharts(stockData.value);
  } catch (error) {
    console.error('Failed to fetch stock details:', error);
  }
}
function createCharts(data) {
  createChart(
    'volumeChart',
    '成交量',
    data.map((d) => d['日期']),
    data.map((d) => parseFloat(d['成交量'])),
    'red',
  );
  createChart(
    'turnoverChart',
    '成交额',
    data.map((d) => d['日期']),
    data.map((d) => parseFloat(d['成交额'])),
    'blue',
  );
  createChart(
    'highPriceChart',
    '最高价',
    data.map((d) => d['日期']),
    data.map((d) => parseFloat(d['最高价'])),
    'green',
  );
  createChart(
    'lowPriceChart',
    '最低价',
    data.map((d) => d['日期']),
    data.map((d) => parseFloat(d['最低价'])),
    'yellow',
  );
  createChart(
    'openPriceChart',
    '开盘价',
    data.map((d) => d['日期']),
    data.map((d) => parseFloat(d['今开'])),
    'purple',
  );
  createChart(
    'closePriceChart',
    '收盘价',
    data.map((d) => d['日期']),
    data.map((d) => parseFloat(d['昨收'])),
    'orange',
  );
}

function createChart(canvasId, label, labels, data, borderColor) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: label,
          data: data,
          borderColor: borderColor,
          borderWidth: 1,
          pointRadius: 4, // 设定点的基础半径
          pointHoverRadius: 6, // 设定悬停时点的半径
          hitRadius: 10, // 增大命中半径，使鼠标更容易触发点的信息显示
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'nearest',
        intersect: false, // 设置为 false 以便在点的附近悬停时也能显示信息
      },
      scales: {
        y: {
          beginAtZero: false,
        },
      },
      plugins: {
        tooltip: {
          enabled: true,
          mode: 'index',
          intersect: false,
        },
      },
    },
  });
}

function goBack() {
  router.push('/index/查询'); // 根据您的路由结构调整路径
}
</script>

<style>
canvas {
  width: 100% !important;
  height: 80% !important;
}
</style>
