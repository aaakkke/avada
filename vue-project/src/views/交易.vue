<template>
  <div class="about" style="height: calc(100vh - 60px); overflow-y: auto">
    <div class="table-gap"></div>
    <el-button type="primary" :icon="CirclePlus" round plain @click="toggleForm">添加交易</el-button>
    <el-button type="primary" :icon="DocumentCopy" round plain @click="fetchAssetInfo">资产交易信息</el-button>

    <br />
    <el-form v-if="showForm" style="max-width: 600px" label-width="auto" :label-position="labelPosition" :size="size">
      <el-form-item label="是否选用策略">
        <el-switch v-model="value1" @change="fetchStrategies" />
      </el-form-item>
      <template v-if="value1">
        <el-form-item label="策略选择">
          <el-select v-model="selectedStrategy" placeholder="请用策略进行交易">
            <el-option v-for="strategy in strategies" :key="strategy.value" :label="strategy.label" :value="strategy.value" />
          </el-select>
        </el-form-item>
        <!-- 动态显示策略参数 -->
        <template v-for="(value, key) in strategyParameters" :key="key">
          <template v-if="key !== '策略名称'">
            <el-form-item :label="key">
              <!-- 如果参数是开始时间或结束时间，使用日期选择器 -->

              <template v-if="key === '开始时间' || key === '结束时间'">
                <el-date-picker v-model="strategyParameters[key]" type="date" placeholder="选择日期" style="width: 100%" />
              </template>
              <!-- 其他类型的参数使用普通输入框 -->
              <template v-else> <el-input v-model="strategyParameters[key]" /> </template>
            </el-form-item>
          </template>
        </template>
      </template>
      <template v-if="!value1">
        <!-- 当策略开关关闭时，显示默认策略参数 -->
        <template v-for="(value, key) in strategyParameters" :key="key">
          <!-- 忽略策略名称 -->
          <template v-if="key !== '策略名称'">
            <el-form-item :label="key">
              <!-- 使用普通输入框展示参数值 -->
              <el-input v-model="strategyParameters[key]" />
            </el-form-item>
          </template>
        </template>
      </template>

      <el-form-item>
        <el-button type="primary" @click="onSubmit">提交交易订单</el-button>
        <el-dialog v-model="dialogVisible" title="提示" width="500">
          <span>您已经成功保存修改</span>
          <template #footer>
            <div class="dialog-footer">
              <el-button type="primary" @click="closeDialogAndClearForm">关闭</el-button>
            </div>
          </template>
        </el-dialog>
      </el-form-item>
    </el-form>
    <div v-if="showAssetInfo">
      <div class="table-gap"></div>
      <el-row class="my-2">
        <el-col :span="24">
          <el-text type="primary" size="large">资产信息</el-text>
        </el-col>
      </el-row>
      <el-row class="my-2">
        <el-col :span="24">
          <el-text>现有资产: {{ assetData.currentAssets }} / 总资产: {{ assetData.totalAssets }}</el-text>
        </el-col>
      </el-row>
      <el-row class="my-2">
        <el-col :span="24">
          <el-text type="primary" size="large">历史交易记录</el-text>
        </el-col>
      </el-row>
      <el-table :data="assetData.transactions" style="width: 100%">
        <el-table-column fixed type="index" width="50" />
        <el-table-column prop="交易时间" label="交易时间" width="180"></el-table-column>
        <el-table-column prop="股票代码" label="股票代码" width="180"></el-table-column>
        <el-table-column prop="股票名称" label="名称" width="180"></el-table-column>
        <el-table-column prop="交易金额" label="交易金额" width="180"></el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { CirclePlus, DocumentCopy } from '@element-plus/icons-vue';
import { reactive, ref, watch } from 'vue';
import axios from 'axios';
import type { ComponentSize, FormProps } from 'element-plus';

const size = ref<ComponentSize>('default');
const labelPosition = ref<FormProps['labelPosition']>('top' as FormProps['labelPosition']);
const showForm = ref(false); // 控制表单显示的响应式变量
const strategies = ref([]); // 存储从后端获取的策略列表
const value1 = ref(false); // 控制策略选择部分的显示
const selectedStrategy = ref('');
const strategyParameters = reactive({});
const dialogVisible = ref(false); // 对话框可见性控制
const showAssetInfo = ref(false); // 控制资产信息显示的响应式变量

const assetData = reactive({
  currentAssets: 0,
  totalAssets: 0,
  transactions: [],
});

function toggleForm() {
  showForm.value = !showForm.value;
  if (!showForm.value) {
    // 如果表单被关闭，则重置状态和策略参数
    value1.value = false; // 默认不使用策略
    resetStrategyParameters(); // 重置策略参数
  }
}
function resetStrategyParameters() {
  // 设置默认策略参数，当策略开关为关闭状态时
  Object.assign(strategyParameters, {
    买入卖出: '买入',
    资金: 10000,
    策略名称: 'None', // 这将在UI中不显示
    股票代码: '600036.SS',
  });
}

async function fetchStrategies(newValue) {
  if (newValue) {
    // 当开关开启时，正常加载策略
    try {
      const response = await axios.post('http://127.0.0.1:5000/strategy_list');
      console.log(response.data);
      // 确保这里正确地访问策略列表数据
      strategies.value = response.data.strategy_list
        .filter((strategy) => strategy.state) // 确保 state 为 true
        .map((strategy) => ({
          label: strategy.name,
          value: strategy.name,
        }));
    } catch (error) {
      console.error('获取策略列表时发生错误：', error);
    }
  } else {
    // 当开关关闭时，设置默认参数
    Object.assign(strategyParameters, {
      买入卖出: '买入',
      初始资金: 10000,
      策略名称: 'None',
      股票代码: '600036.SS',
    });
  }
}

// 在对话框关闭时调用此函数
function closeDialogAndClearForm() {
  dialogVisible.value = false;
  showForm.value = false; // 隐藏表单
  selectedStrategy.value = ''; // 重置选定的策略
  value1.value = false; // 重置策略开关
  Object.keys(strategyParameters).forEach((key) => {
    delete strategyParameters[key]; // 清空策略参数
  });
}
watch(selectedStrategy, (newVal) => {
  if (newVal) {
    fetchStrategyParameters();
  }
});

async function fetchStrategyParameters() {
  try {
    const response = await axios.post('http://127.0.0.1:5000/deal1', { strategy_name: selectedStrategy.value });
    const newParameters = response.data.parameter[0];
    // 清空既有属性
    for (const key in strategyParameters) {
      delete strategyParameters[key];
    }
    // 将新对象的属性复制到strategyParameters中
    Object.assign(strategyParameters, newParameters);
    console.log(strategyParameters);
  } catch (error) {
    console.error('获取策略参数时发生错误：', error);
  }
}

async function onSubmit() {
  console.log('Submitting:', strategyParameters);
  // 调用函数发送策略参数到后端
  await submitStrategyParameters();
}
// 新函数：提交策略参数到后端
async function submitStrategyParameters() {
  try {
    const response = await axios.post('http://127.0.0.1:5000/submit_strategy', { strategyParameter: strategyParameters });
    console.log('Response from server:', response.data);
    // 可以在这里添加任何后续逻辑，比如清空表单、显示成功消息等
    if (response.data.state === 'successfully') {
      // 根据后端返回的状态显示对话框
      dialogVisible.value = true;
    }
  } catch (error) {
    console.error('提交策略参数时发生错误：', error);
  }
}

async function fetchAssetInfo() {
  try {
    const response = await axios.post('http://127.0.0.1:5000/asset_info'); // 修改为你的后端API地址
    console.log(response.data);
    // 根据需要处理和显示资产和交易记录数据
    assetData.currentAssets = response.data.current_assets;
    assetData.totalAssets = response.data.total_assets;
    assetData.transactions = response.data.transactions;
    showAssetInfo.value = true; // 显示资产信息
  } catch (error) {
    console.error('获取资产交易信息时发生错误：', error);
    showAssetInfo.value = false; // 发生错误时不显示资产信息
  }
}
</script>

<style>
.table-gap {
  height: 30px; /* 设置间隙高度 */
}
.about {
  padding: 0 20px; /* 添加左右内边距为20px */
}
</style>
