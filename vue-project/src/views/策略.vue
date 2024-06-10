<template>
  <div style="height: 100%; width: 100%">
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
          <el-button type="primary" size="small" plain :icon="Search" @click="editItem(scope.row)">code</el-button>
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
    <div class="table-gap"></div>
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
          <el-button type="primary" size="small" plain :icon="Search" @click="editItem(scope.row)">code</el-button>
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
    <div class="table-gap"></div>

    <el-button type="primary" plain @click="saveSelection"> 保存选用 </el-button>
    <el-dialog v-model="dialogVisible" title="提示" width="500">
      <span>您已经成功保存修改</span>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="dialogVisible = false">关闭</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { Search, CircleCheck, CircleClose } from '@element-plus/icons-vue';
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
const router = useRouter();
const tableData = ref([]);
const dialogVisible = ref(false);

const editItem = (row: any) => {
  router.push(`/策略代码/${row.name}`);
};

onMounted(() => {
  fetchStrategyData();
});

const fetchStrategyData = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:5000/strategy_list', { name: 'kkkeee' });
    console.log(response.data);
    tableData.value = response.data.strategy_list;
  } catch (error) {
    console.error('获取策略列表时发生错误：', error);
  }
};

const toggleSelect = (row: any) => {
  row.state = !row.state;
};

const saveSelection = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:5000/confirm', {
      data: tableData.value,
    });
    if (response.data.message == 'successfully') {
      dialogVisible.value = true;
    }
  } catch (error) {
    console.error('保存选用时发生错误：', error);
  }
};
</script>

<style lang="scss">
.mx-1 {
  margin-left: 5px;
  margin-right: 5px;
}
.table-gap {
  height: 30px; /* 设置间隙高度 */
}
</style>
