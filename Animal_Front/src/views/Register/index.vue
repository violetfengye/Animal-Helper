<template>
  <div class="register-container">
    <div class="form-wrapper">
      <el-card class="box-card">
        <template #header>
          <el-button type="text" class="back-login" @click="ToLogin">
            <el-icon><Back /></el-icon>返回登录
          </el-button>
          <div class="card-header">
            <span class="title">用户注册</span>
          </div>
        </template>

        <el-tabs v-model="activeTab" @tab-change="handleTabChange">
          <!-- 用户注册 -->
          <el-tab-pane label="用户注册" name="common_user">
            <el-form
              ref="common_userFormRef"
              :model="common_userForm"
              :rules="common_userRules"
              label-position="top"
            >
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="用户名" prop="username">
                    <el-input
                      v-model="common_userForm.username"
                      placeholder="4-16位字母数字组合"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="密码" prop="password">
                    <el-input
                      v-model="common_userForm.password"
                      type="password"
                      show-password
                      placeholder="至少6位字符"
                    />
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="姓名" prop="name">
                    <el-input v-model="common_userForm.name" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="性别" prop="gender">
                    <el-select
                      v-model="common_userForm.gender"
                      placeholder="请选择"
                    >
                      <el-option label="男" value="male" />
                      <el-option label="女" value="female" />
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="邮箱" prop="email">
                    <el-input v-model="common_userForm.email" type="email" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="手机号" prop="phone">
                    <el-input v-model="common_userForm.phone" />
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="用户id" prop="common_user_id">
                    <el-input v-model="common_userForm.common_user_id" />
                  </el-form-item>
                </el-col>
              </el-row>
            </el-form>
          </el-tab-pane>

          <!-- 管理员注册 -->
          <el-tab-pane label="管理员注册" name="admin">
            <el-form
              ref="adminFormRef"
              :model="adminForm"
              :rules="adminRules"
              label-position="top"
            >
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="用户名" prop="username">
                    <el-input v-model="adminForm.username" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="密码" prop="password">
                    <el-input
                      v-model="adminForm.password"
                      type="password"
                      show-password
                    />
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="姓名" prop="name">
                    <el-input v-model="adminForm.name" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="性别" prop="gender">
                    <el-select v-model="adminForm.gender" placeholder="请选择">
                      <el-option label="男" value="male" />
                      <el-option label="女" value="female" />
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="邮箱" prop="email">
                    <el-input v-model="adminForm.email" type="email" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="手机号" prop="phone">
                    <el-input v-model="adminForm.phone" />
                  </el-form-item>
                </el-col>
              </el-row>

              <el-form-item label="管理员管理员编号" prop="admin_id">
                <el-input v-model="adminForm.admin_id" />
              </el-form-item>
            </el-form>
          </el-tab-pane>
        </el-tabs>

        <div class="submit-btn">
          <el-button type="primary" size="large" @click="handleSubmit">
            立即注册
          </el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { ElMessage } from "element-plus";
import router from "../../router";
import { UserRegister } from "../../api/index.ts";
import { Back } from "@element-plus/icons-vue";

const activeTab = ref("common_user");

const common_userFormRef = ref(null);
const adminFormRef = ref(null);

const common_userForm = reactive({
  username: "",
  password: "",
  name: "",
  gender: "",
  email: "",
  phone: "",
  common_user_id: "",
});

const adminForm = reactive({
  username: "",
  password: "",
  name: "",
  gender: "",
  email: "",
  phone: "",
  admin_id: "",
});

function ToLogin() {
  router.replace("/login");
}

// 用户验证规则
const common_userRules = reactive({
  username: [
    { required: true, message: "请输入用户名", trigger: "blur" },
    { min: 4, max: 16, message: "长度在4到16个字符", trigger: "blur" },
  ],
  password: [
    { required: true, message: "请输入密码", trigger: "blur" },
    { min: 6, message: "密码长度至少6位", trigger: "blur" },
  ],
  name: [{ required: true, message: "请输入姓名", trigger: "blur" }],
  gender: [{ required: true, message: "请选择性别", trigger: "change" }],
  email: [
    { required: true, message: "请输入邮箱", trigger: "blur" },
    { type: "email", message: "请输入正确的邮箱格式", trigger: "blur" },
  ],
  phone: [
    { required: true, message: "请输入手机号", trigger: "blur" },
    { pattern: /^1[3-9]\d{9}$/, message: "手机号格式不正确", trigger: "blur" },
  ],
  common_user_id: [{ required: true, message: "请输入用户编号", trigger: "blur" }],
});

// 管理员验证规则
const adminRules = reactive({
  username: [
    { required: true, message: "请输入用户名", trigger: "blur" },
    { min: 4, max: 16, message: "长度在4到16个字符", trigger: "blur" },
  ],
  password: [
    { required: true, message: "请输入密码", trigger: "blur" },
    { min: 6, message: "密码长度至少6位", trigger: "blur" },
  ],
  name: [{ required: true, message: "请输入姓名", trigger: "blur" }],
  gender: [{ required: true, message: "请选择性别", trigger: "change" }],
  email: [
    { required: true, message: "请输入邮箱", trigger: "blur" },
    { type: "email", message: "请输入正确的邮箱格式", trigger: "blur" },
  ],
  phone: [
    { required: true, message: "请输入手机号", trigger: "blur" },
    { pattern: /^1[3-9]\d{9}$/, message: "手机号格式不正确", trigger: "blur" },
  ],
  admin_id: [{ required: true, message: "请输入管理员编号", trigger: "blur" }],
});

const handleTabChange = () => {
  // 切换时清空表单
  if (activeTab.value === "common_user") {
    Object.keys(common_userForm).forEach((key) => (common_userForm[key] = ""));
  } else {
    Object.keys(adminForm).forEach((key) => (adminForm[key] = ""));
  }
};

const handleSubmit = () => {
  const formRef =
    activeTab.value === "common_user" ? common_userFormRef : adminFormRef;

  // 执行表单验证
  formRef.value.validate().then((valid) => {
    if (!valid) {
      ElMessage.error("您提供的信息有误");
      return;
    }
    const formData =
      activeTab.value === "common_user" ? common_userForm : adminForm;
    // 转换性别字段
    if (formData.gender === "男") {
      formData.gender = "male";
    } else if (formData.gender === "女") {
      formData.gender = "female";
    }
    // 提交逻辑
    const registerFunction =
      activeTab.value === "common_user"
        ? UserRegister.common_userRegisterApi
        : UserRegister.adminRegisterApi;

    registerFunction(formData).then((response) => {
      // 如果返回的响应状态码不是200，则显示错误信息并结束函数
      if (response.code !== 200) {
        ElMessage.error(response.msg);
        return;
      }
      // 显示登录成功的消息
      ElMessage.success("注册成功");
      router.replace("/login");
    });
  });
};
</script>

<style scoped>
.back-login {
  position: flex;

  font-size: 14px;
  color: #409eff;
  cursor: pointer;
}

.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f0f2f5;
}

.form-wrapper {
  width: 800px;
  padding: 20px;
}

.box-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  text-align: center;
  padding: 20px 0;
}

.title {
  font-size: 24px;
  font-weight: 500;
  color: #303133;
}

.submit-btn {
  text-align: center;
  margin-top: 30px;
}

.el-button {
  width: 200px;
  height: 40px;
}
</style>
