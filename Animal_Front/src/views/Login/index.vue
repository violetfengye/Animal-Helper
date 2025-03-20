<template>
  <div class="main">
    <div class="login-main-box">
      <!-- 轮播图 -->
      <div class="login-left-box">
        <el-carousel height="calc(100vh - 200px)" style="width: 100%">
          <el-carousel-item v-for="item in carouseGroup" :key="item.id">
            <div class="carousel-item-box">
              <div class="carousel-item-desc-box">
                <span class="carousel-item-desc-title">{{ item.title }}</span>
                <span class="carousel-item-desc-content">{{
                  item.content
                }}</span>
              </div>
              <el-image style="width: 60%" :src="item.imagePath" fit="cover" />
            </div>
          </el-carousel-item>
        </el-carousel>
      </div>

      <!--      登录界面-->
      <div class="login-right-box">
        <!-- logo -->
        <div class="login-right-common login-right-logo-box">
          <div class="logo-content">
            <el-image
              style="width: 70px"
              src="/src/images/ExamOnlineLogo.png"
              fit="cover"
            />
            <div
              style="display: flex; flex-direction: column; margin-left: 5px"
            >
              <span class="logo-wording-item">动物管理系统</span>
              <span class="logo-wording-item-en">Position Alert Welfare</span>
            </div>
          </div>
        </div>

        <div class="login-right-common login-right-form-box">
          <!-- 新增管理员登录按钮 -->
          <div v-if="!isSuperAdministrator" class="admin-login-link">
            <el-link type="primary" @click="goAdminLogin">
              <UserRound class="admin-icon" />
              超级管理员登录
            </el-link>
          </div>
          <!-- 管理员模式显示 -->
          <div v-else class="admin-mode-header">
            <span class="form-title-wording">超级管理员登录</span>
            <el-link
              type="info"
              class="admin-login-link"
              @click="ToCommonLogin"
            >
              返回普通登录
            </el-link>
          </div>

          <span class="form-title-wording" v-if="!isSuperAdministrator"
            >欢迎登录</span
          >

          <div class="login-select-role-group" v-if="!isSuperAdministrator">
            <div
              class="select-role-item select-active-item"
              @click="handleActiveCommon_user"
            >
              用户
            </div>
            <div
              class="select-role-item"
              style="padding-left: 20px"
              @click="handleActiveAdmin"
            >
              管理员
            </div>
          </div>

          <div class="login-select-role-group" v-else>
            <div class="select-role-item select-active-item">管理员</div>
          </div>

          <div style="width: 85%; margin-top: 20px">
            <el-form label-position="top" label-width="auto" :model="formLogin">
              <el-form-item label="用户名">
                <el-input v-model="formLogin.username" size="large">
                  <template #prefix>
                    <UserRound style="width: 16px" />
                  </template>
                </el-input>
              </el-form-item>
              <el-form-item label="密码">
                <el-input
                  v-model="formLogin.password"
                  show-password
                  size="large"
                >
                  <template #prefix>
                    <LockKeyhole style="width: 16px" />
                  </template>
                </el-input>
              </el-form-item>
              <el-form-item v-if="!isSuperAdministrator">
                <el-checkbox v-model="formLogin.rememberPass"
                  >记住密码</el-checkbox
                >
              </el-form-item>
            </el-form>
            <el-button
              type="primary"
              style="width: 100%; margin-top: 15px"
              size="large"
              @click="handleLogin"
            >
              <LogIn class="common-btn-icon-style" />
              登 录
            </el-button>
          </div>
          <el-button
            v-if="!isSuperAdministrator"
            type="Default"
            style="width: 85.5%; margin-top: 15px"
            size="large"
            @click="ToRegister"
          >
            <el-icon class="common-btn-icon-style"><Pointer /></el-icon>
            前去注册
          </el-button>
        </div>
        <div class="login-right-common login-right-end"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { router } from "../../router";
import { onMounted, reactive, computed, watchEffect, toRef } from "vue";
import { ElMessage } from "element-plus";
import { Pointer } from "@element-plus/icons-vue";
import { UserLogin } from "../../api/index.ts";
import { LockKeyhole, UserRound, LogIn } from "lucide-vue-next";
import { setCookie } from "../../utils/cookie.ts";
import { useUserStatu } from "../../stores/AuthStatu.ts";

// 从当前路由获取是否为管理员登录标志
// const isSuperAdministrator = router.currentRoute.value.query?.admin
const isSuperAdministrator = computed(
  () => router.currentRoute.value.query?.super_admin === "true"
);

// 轮播图信息组
const carouseGroup = [
  {
    id: 0,
    imagePath: "src/images/c1.png",
    title: "科技温度，为无声者发声",
    content:
      "在校园的隐秘角落，无数流浪猫狗正与饥饿、伤病和未知风险无声抗争。我们以物联网为笔，为生命书写希望。每一次数据波动都是生命的呼救，每一道预警信号都在改写流浪的命运。在这里，硬核科技化作最温柔的守望者。",
  },
  {
    id: 1,
    imagePath: "src/images/c2.png",
    title: "从被动到主动，重构救助逻辑",
    content:
      "传统救助往往困于人力与信息的滞后，而我们的系统让善意跑在危机之前。当AI通过步态分析秒级响应骨折风险，当消瘦数据自动触发周边志愿者接单补粮——技术正将「事后补救」转化为「事前防御」。"
  },
  {
    id: 2,
    imagePath: "src/images/c3.png",
    title: "智慧生态，让善意精准抵达",
    content:
      "这不仅是覆盖校园的动物健康监测网，更是一场公益管理的范式革新。云端大屏实时定位高危个体，动态调配粮药资源；AI溯源传染病风险，为群体构筑免疫屏障。我们让冰冷的数据流淌暖意，用精准算法串联起设备、机构与千万爱心。"
  },
];

// 登录信息Form表单
const formLogin = reactive({
  username: "",
  password: "",
  rememberPass: false,
  isSuperAdmin: false, // 标志是否为管理员
});

const userStatuStore = useUserStatu();

const loginRole = toRef(userStatuStore.role);

watchEffect(() => {
  formLogin.isSuperAdmin = isSuperAdministrator.value;
  if (formLogin.isSuperAdmin) {
    loginRole.value = "SuperAdmin";
  } else {
    loginRole.value = "Common_user";
  }
});

// 处理记住密码时的数据回写
const handleRemember = () => {
  if (!isSuperAdministrator.value) {
    formLogin.isSuperAdmin = false;
    const { ROLE, LOGIN_INFO } = localStorage; // 解构出 localStorage 对象中的 ROLE 和 LOGIN_INFO 属性
    if (ROLE && LOGIN_INFO) {
      // 如果 ROLE 和 LOGIN_INFO 存在
      const role = ROLE; // 读取 ROLE
      const loginInfo = JSON.parse(LOGIN_INFO); // 解析 LOGIN_INFO 字符串为对象
      if (role === "Common_user") {
        handleActiveCommon_user();
      } else {
        handleActiveAdmin();
      }
      Object.assign(formLogin, loginInfo); // 将解析后的登录信息合并到 formLogin 对象中
    }
  }
};

// 新增路由跳转方法
const goAdminLogin = () => {
  router.push({
    path: "/login",
    query: { super_admin: "true" },
  });
  formLogin.isSuperAdmin = true;
};

function ToCommonLogin() {
  router.push({
    path: "/login",
  });
  formLogin.isSuperAdmin = false;
}

function ToRegister() {
  router.replace("/register");
}

onMounted(() => {
  handleRemember();
});

// 处理激活的登录角色
const handleActiveRole = (index: number) => {
  if (!isSuperAdministrator.value) {
    const roleItems = document.getElementsByClassName("select-role-item");
    const activeItemClass = "select-active-item";
    // 添加 select-active-item 类到指定索引的元素
    roleItems[index].classList.add(activeItemClass);
    // 移除 select-active-item 类从另一个元素
    const otherIndex = index === 0 ? 1 : 0;
    roleItems[otherIndex].classList.remove(activeItemClass);
  }
};

// 处理用户角色
const handleActiveCommon_user = () => {
  handleActiveRole(0); // 角色类型索引为 0 表示用户
  loginRole.value = "Common_user";
};

// 处理老师角色
const handleActiveAdmin = () => {
  handleActiveRole(1); // 角色类型索引为 1 表示老师
  loginRole.value = "Admin";
};

// 处理登录
const handleLogin = () => {
  // 根据用户选择的角色确定调用的登录函数

  console.log(loginRole.value);

  const loginFunction =
    loginRole.value === "Common_user"
      ? UserLogin.common_userLoginApi
      : UserLogin.adminLoginApi;

  // 调用相应的登录函数
  loginFunction(formLogin).then((response) => {
    // 如果返回的响应状态码不是200，则显示错误信息并结束函数
    if (response.code !== 200) {
      ElMessage.error(response.msg);
      return;
    }
    // 显示登录成功的消息
    ElMessage.success("登录成功");
    // 存储Access Token
    localStorage.setItem("TOKEN", response.data["access"]);
    // 存储角色信息
    localStorage.setItem("ROLE", loginRole.value);
    // 存储登录信息（登录人的姓名）
    const userInfo = {
      userId: response.data["userId"],
      username: response.data["name"],
    };
    setCookie("UserInfo", JSON.stringify(userInfo));
    // 如果用户选择了记住密码，则将登录信息存储到localStorage中，否则清除localStorage中的登录信息
    if (formLogin.rememberPass) {
      localStorage.setItem("LOGIN_INFO", JSON.stringify(formLogin));
    } else {
      localStorage.removeItem("LOGIN_INFO");
    }
    router.replace("/homepage");
  });
};
</script>

<style scoped lang="scss">
@import "../../style.scss";

.admin-login-link {
  position: absolute;
  bottom: 10px;

  display: flex;
  align-items: center;
  cursor: pointer;

  .admin-icon {
    width: 14px;
    margin-right: 5px;
  }

  :deep(.el-link) {
    font-size: 14px;
  }
}

.login-right-form-box {
  position: relative; // 新增定位上下文
  /* 其他样式保持不变 */
}

.login-main-box {
  width: 100%;
  height: 100vh;
  display: flex;
}
.login-left-box {
  @include baseFlexStyle {
    background-color: #fff;
    align-items: center;
  }
  .carousel-item-box {
    @include baseFlexStyle {
      justify-content: center;
      flex-direction: column;
      align-items: center;
    }
    .carousel-item-desc-box {
      width: 80%;
      display: flex;
      color: #3e3e3e;
      flex-direction: column;
      letter-spacing: 3px;
      .carousel-item-desc-title {
        font-size: 36px;
        margin-bottom: 20px;
      }
      .carousel-item-desc-content {
        font-size: 18px;
      }
    }
  }
}
.login-right-box {
  width: 35%;
  min-width: 580px;
  flex: 0 0 auto;
  background-color: #d9ecff;
  display: flex;
  flex-direction: column;
  padding: 0 50px;
  .login-right-common {
    width: 100%;
  }
}
.login-right-logo-box {
  display: flex;
  flex: 2 1 auto;
  position: relative;
  flex-direction: column;
  &::before {
    height: 80px;
    display: block;
    content: "";
  }
  &::after {
    flex: 2 1 auto;
    display: block;
    content: "";
  }
  .logo-content {
    display: flex;
    align-items: center;
    .logo-wording-item {
      font-size: 20px;
      color: #3e3e3e;
      letter-spacing: 2px;
    }
    .logo-wording-item-en {
      font-size: 10px;
      color: #3e3e3e;
      letter-spacing: 2px;
    }
  }
}
.login-right-form-box {
  height: 550px;
  display: flex;
  flex: 0 0 auto;
  flex-direction: column;
  align-items: center;
  .form-title-wording {
    font-size: 18px;
    color: #337ecc;
    letter-spacing: 3px;
    font-weight: bolder;
  }
  .login-select-role-group {
    display: flex;
    margin-top: 28px;
    letter-spacing: 3px;
    .select-role-item {
      color: #3e3e3e;
      font-size: 18px;
      padding: 0 18px 8px 18px;
      position: relative;
      cursor: pointer;
    }
  }
}
.login-right-end {
  flex: 3 1 auto;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}
.select-active-item {
  &::after {
    position: absolute;
    content: "";
    width: 50px;
    height: 3px;
    background: #79bbff;
    left: calc(50% - 27px);
    bottom: 0;
    border-radius: 4px;
  }
}
</style>
