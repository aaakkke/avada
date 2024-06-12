<template>
  <div id="backcont">
    <div class="window">
      <div class="login-window">
        <div class="title" style="margin-left: 80px">阿瓦达量化交易平台</div>
        <el-form ref="ruleFormRef" style="max-width: 450px; overflow-y: auto" :model="ruleForm" status-icon :rules="rules" label-width="auto" class="demo-ruleForm">
          <el-form-item label="账号" prop="username">
            <el-input v-model.number="ruleForm.username" />
          </el-form-item>
          <el-form-item label="密码" prop="pass">
            <el-input v-model="ruleForm.pass" type="password" autocomplete="off" />
          </el-form-item>
          <el-form-item label="确认密码" prop="checkPass">
            <el-input v-model="ruleForm.checkPass" type="password" autocomplete="off" />
          </el-form-item>
          <el-form-item label="初始基金" prop="money">
            <el-input v-model.number="ruleForm.money" />
          </el-form-item>
          <el-form-item label="风险等级">
            <el-select v-model="value" placeholder="Select" size="large" style="width: 240px">
              <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
        </el-form>
        <!--注册登录切换-->
        <router-link to="/login" class="point">
          <el-button type="success" plain class="registerview">返回</el-button>
        </router-link>
        <el-button type="success" @click="submitForm(ruleFormRef)" class="loginbutton">注册</el-button>
      </div>
    </div>
  </div>
</template>
<script lang="ts" setup>
import { reactive, ref } from 'vue';
import type { FormInstance, FormRules } from 'element-plus';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import router from '@/router';

const ruleFormRef = ref<FormInstance>();
const checkusername = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error('请输入用户名'));
  } else {
    console.log('good username');
    callback();
  }
};
const checkmoney = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error('请输入初始基金'));
  } else if (!Number.isInteger(value)) {
    callback(new Error('请输入数字'));
  } else {
    console.log('good money');
    callback();
  }
};

const validatePass = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请输入密码'));
  } else {
    if (ruleForm.checkPass !== '') {
      if (!ruleFormRef.value) return;
      ruleFormRef.value.validateField('checkPass');
    }
    console.log('good pass');
    callback();
  }
};
const validatePass2 = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入密码'));
  } else if (value !== ruleForm.pass) {
    callback(new Error('两次密码输入不一致'));
  } else {
    console.log('good checkpass');
    callback();
  }
};

const ruleForm = reactive({
  username: '',
  pass: '',
  checkPass: '',
  money: '',
});

const rules = reactive<FormRules<typeof ruleForm>>({
  pass: [{ validator: validatePass, trigger: 'blur' }],
  checkPass: [{ validator: validatePass2, trigger: 'blur' }],
  username: [{ validator: checkusername, trigger: 'blur' }],
  money: [{ validator: checkmoney, trigger: 'blur' }],
});

const submitForm = (formEl: FormInstance | undefined) => {
  console.log('press');
  if (!formEl) return;
  formEl.validate(async (valid) => {
    console.log('valid:', valid);
    if (valid) {
      console.log('submit!');
      console.log(ruleForm.username, ruleForm.pass, value.value, ruleForm.money);
      try {
        const response = await axios.post('http://127.0.0.1:5000/register', {
          username: ruleForm.username,
          password: ruleForm.pass,
          money: ruleForm.money,
          riskLevel: value.value,
        });
        if (response.status === 201) {
          console.log('用户注册成功');
          ElMessage(response.data.msg);
          router.push('/login');
        } else if (response.status === 400) {
          console.log('用户名已存在或JSON格式无效');
          ElMessage(response.data.msg);
        } else {
          console.log('其他错误');
        }
      } catch (error) {
        console.error('请求失败', error);
      }
    }
  });
};

const value = ref('');
const options = [
  {
    value: 'Option1',
    label: 'Option1',
  },
  {
    value: 'Option2',
    label: 'Option2',
  },
  {
    value: 'Option3',
    label: 'Option3',
  },
  {
    value: 'Option4',
    label: 'Option4',
  },
];
</script>
<style>
#backcont {
  background: url(@/assets/background.png) no-repeat scroll 50% 0 transparent;
  width: 100vw;
  height: 100vh;
  background-position-x: 0%;
  background-position-y: 0%;
  margin: 0;
  padding: 0;
  background-size: 100% 100%;
  overflow: hidden;
}
.window {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.login-window {
  width: 550px;
  height: 400px;
  padding-left: 35px;
  background: #f0f2f5;
  border-radius: 10px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border: 1px solid #ccc;
  overflow-y: auto;
}
.title {
  color: #333;
  font-size: 36px;
  padding-top: 20px;
  font-family: '幼圆', Arial, Helvetica, sans-serif;
  font-weight: bold;
}
.user {
  width: 400px;
  margin: 0 auto;
  margin-bottom: 17px;
  padding-top: 30px;
  height: 40px;
  display: flex;
  align-items: center;
}
.inptflex {
  display: inline-block;
}
.registerview {
  width: 50px;
  position: absolute;
  left: 7%;
  top: 330px;
  padding-top: 10px;
  cursor: pointer;
  box-sizing: border-box;
}
.loginbutton {
  width: 200px;
  position: absolute;
  top: 330px;
  left: 50%;
  transform: translateX(-50%);
}
.point {
  display: block;
  width: 50px;
}
</style>
