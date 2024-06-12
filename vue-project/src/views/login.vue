<template>
  <div id="backcont">
    <div class="window">
      <div class="login-window">
        <div class="title" style="margin-left: 80px">阿瓦达量化交易平台</div>
        <div class="table-gap"></div>
        <div class="user">账号<el-input clearable v-model="user.account" class="inptflex" placeholder="请输入账号" /></div>
        <div class="user">密码<el-input show-password v-model="user.password" class="inptflex" placeholder="请输入密码" /></div>
        <!--注册登录切换-->
        <el-button type="success" plain class="registerview" @click="register">注册</el-button>
        <el-button @click="signin" type="success" class="loginbutton">登录</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';

export default {
  setup() {
    const router = useRouter();
    const user = reactive({
      account: '',
      password: '',
    });

    const signin = async () => {
      console.log(user.account, user.password);
      try {
        const response = await axios.post('http://127.0.0.1:5000/login', {
          username: user.account,
          password: user.password,
        });
        console.log(response.data);
        if (response.status === 200) {
          console.log('登录成功');
          // 跳转到主页面
          router.push('/index');
        } else {
          console.log('用户名或密码错误');
          ElMessage(response.data.msg);
        }
      } catch (error) {
        console.error('请求失败', error);
      }
    };

    const register = () => {
      router.push('/register');
    };

    return {
      user,
      signin,
      register,
    };
  },
};
</script>

<style>
.table-gap {
  height: 50px; /* 设置间隙高度 */
}
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
  margin-left: 400px;
  padding-top: 10px;
  cursor: pointer;
  box-sizing: border-box;
}
.loginbutton {
  width: 200px;
  position: absolute;
  top: 240px;
  left: 50%;
  transform: translateX(-50%);
}
.point {
  display: block;
  width: 50px;
}
</style>
