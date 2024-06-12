<template>
  <div style="margin-top: 10px"></div>
  <el-text class="mx-1" type="primary" size="large" style="margin-left: 10px">用户信息</el-text>
  <div style="margin-top: 10px"></div>
  <div style="margin-left: 15px">
    <el-form :model="form" label-width="auto" style="max-width: 600px">
      <el-form-item label="用户名">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="form.password" />
      </el-form-item>
      <el-form-item label="风险等级">
        <el-select v-model="form.region" placeholder="please select your zone">
          <el-option label="1" value="1" />
          <el-option label="2" value="2" />
          <el-option label="3" value="3" />
          <el-option label="4" value="4" />
        </el-select>
      </el-form-item>
      <el-form-item label="初始资金">
        <el-input v-model="form.fund" />
      </el-form-item>
      <el-form-item style="margin-left: 255px; margin-top: 5px">
        <el-button type="primary" @click="submitForm">保存修改</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'; // 引入 ref 和 onMounted
import axios from 'axios';
export default {
  setup() {
    const form = ref({
      name: '',
      password: '',
      fund: '',
      region: '1', // 初始值应该是字符串类型
    });

    onMounted(() => {
      getUserInfo(form);
    });

    async function getUserInfo(form) {
      try {
        console.log('111');
        const response = await axios.post('http://127.0.0.1:5000/user-info');
        console.log(response.data);
        if (response.data) {
          const user_info = response.data.user_info;
          form.value.name = user_info['用户名'];
          form.value.password = user_info['密码'];
          form.value.fund = user_info['初始资金'];
          form.value.region = user_info['等级'].toString();
        } else {
          throw new Error('User not found');
        }
      } catch (error) {
        console.error(error);
      }
    }

    async function submitForm() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/user-info-upload', { user_info: form.value });
        if (response.data) {
          ElMessage.success(response.data.msg);
        } else {
          throw new Error('Invalid JSON format');
        }
      } catch (error) {
        console.error(error);
        ElMessage.error(error.message);
      }
    }

    return {
      form,
      submitForm,
    };
  },
};
</script>

<style>
.table-gap {
  height: 30px; /* 设置间隙高度 */
}
</style>
