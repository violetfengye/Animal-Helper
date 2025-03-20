<template>
  <div class="homepage-main-box">
    <div class="homepage-left-box">
      <div class="homepage-login-info-box">
        <span class="homepage-login-info-zh">{{ homePageLoginWording }}</span>
        <span style="font-size: 15px">
          May each day bring you closer to your dreams and fill your life with
          beautiful moments.
        </span>
      </div>

      <div class="homepage-left-main-box" style="padding-bottom: 0">
        <div class="homepage-card-title">
          <el-icon color="#66b1ff"><BookOpenCheck /></el-icon>
          <span>任务信息</span>
        </div>

        <el-divider style="margin-top: 8px" />
        <el-calendar class="calendar-style">
          <!-- 自定义日历日期单元格的内容 -->
          <template #date-cell="{ data }">
            <div style="display: flex; align-items: center">
              <!-- 展示当前日期的日部分（从完整日期字符串中提取） -->
              <span>{{ data.day.split("-")[2] }}</span>

              <!-- 若当前日期存在于 taskDates 数组中，显示任务标记 -->
              <el-icon
                v-if="taskDates.includes(data.day)"
                style="margin-left: 10px"
                color="#ff4d36"
              >
                <!-- 悬停时弹出任务信息的浮层 -->
                <el-popover
                  placement="top-start"
                  title="任务列表"
                  :width="250"
                  trigger="hover"
                >
                  <!-- 定义浮层的触发元素 -->
                  <template #reference><Star /></template>

                  <!-- 若该日期存在任务信息，显示任务列表 -->
                  <div
                    v-if="
                      taskInfoByDate[data.day] &&
                      Object.keys(taskInfoByDate[data.day]).length !== 0
                    "
                  >
                    <!-- 遍历该日期对应的任务数组 -->
                    <div
                      v-for="(item, index) in taskInfoByDate[data.day]"
                      :key="index"
                      class="calendar-popover-content"
                    >
                      <!-- 显示任务名称 -->
                      <span style="margin-bottom: 3px"
                        >任务名称: {{ item.title }}</span
                      >
                      <!-- 显示任务描述 -->
                      <span>任务描述: {{ item.description }}</span>
                      <span>任务状态: {{ item.status }}</span>

                      <!-- 在任务项之间添加分隔线（非最后一个任务时显示） -->
                      <el-divider
                        v-if="index + 1 !== taskInfoByDate[data.day].length"
                        style="margin: 8px 0"
                      />
                    </div>
                  </div>
                </el-popover>
              </el-icon>
            </div>
          </template>
        </el-calendar>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import moment from "moment";
import { onMounted, ref } from "vue";
import { BookOpenCheck, Star } from "lucide-vue-next";
import { getCookie } from "../../utils/cookie.ts";
import { TasksApi } from "../../api";
import { ElMessage } from "element-plus";

// 获取当前日期
const currentDate = moment();
// 获取当前登录人姓名
const userInfo = getCookie("UserInfo") ? JSON.parse(getCookie("UserInfo")) : {};

// 角色信息
const role = localStorage.getItem("ROLE");

// 首页登录信息展示
const homePageLoginWording = ref("");

//存储获取的任务
const taskInfoMultiple = ref<any[]>([]);
// 提取所有的 deadline 到 taskDates 数组
const taskDates = ref<string[]>([]);
// 按日期存储任务信息
const taskInfoByDate = ref<{ [date: string]: any[] }>({});

console.log(taskInfoByDate.value);
// 获取任务信息
const getTaskInfo = () => {
  if (role === "Common_user") {
    homePageLoginWording.value = `欢迎 ${
      userInfo.username
    } 登录！今天是 ${currentDate.format("YYYY-MM-DD")}`;
  } else if (role === "Admin") {
    homePageLoginWording.value = `欢迎 ${
      userInfo.username
    } 登录！今天是 ${currentDate.format("YYYY-MM-DD")}`;
  } else {
    homePageLoginWording.value = `欢迎管理员登录！今天是 ${currentDate.format(
      "YYYY-MM-DD"
    )}`;
  }
  if (role === "Common_user") {
    TasksApi.userGetTaskApi(userInfo.userId).then((response) => {
      if (response.code !== 200) {
        ElMessage.error(response.msg);
        return;
      } else {
        taskInfoMultiple.value = response.data;
        taskInfoMultiple.value.forEach((task) => {
          const deadline = task.deadline.split("T")[0];
          if (!taskDates.value.includes(deadline)) {
            taskDates.value.push(deadline);
          }
          if (!taskInfoByDate.value[deadline]) {
            taskInfoByDate.value[deadline] = [];
          }
          taskInfoByDate.value[deadline].push({
            title: task.title,
            description: task.description,
            status: task.status,
          });
        });
      }
    });
  }
};

onMounted(() => {
  getTaskInfo();
});
</script>

<style scoped lang="scss">
@import "../../style.scss";

.homepage-main-box {
  @include baseFlexStyle;
}
.homepage-left-box {
  @include baseFlexStyle {
    flex-direction: column;
  }

  .homepage-login-info-box {
    height: 120px;
    box-shadow: 0 0 8px rgba(136, 136, 136, 0.5);
    border-radius: 8px;
    margin-bottom: 30px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: #3e3e3e;
    .homepage-login-info-zh {
      font-size: 18px;
      letter-spacing: 2px;
      margin-bottom: 8px;
    }
  }
  .homepage-left-main-box {
    height: calc(100vh - 300px);
    box-shadow: 0 0 8px rgba(136, 136, 136, 0.5);
    border-radius: 8px;
    padding: 20px;
  }
}
.homepage-right-box {
  width: 500px;
  height: calc(100% - 52px);
  box-shadow: 0 0 8px rgba(136, 136, 136, 0.5);
  border-radius: 8px;
  margin-left: 30px;
  padding: 20px;
}
.homepage-card-title {
  margin-left: 10px;
  display: flex;
  align-items: center;
  span {
    margin-left: 8px;
    color: #3e3e3e;
  }
}

.calendar-popover-content {
  font-size: 13px;
  display: flex;
  flex-direction: column;
}

:deep(.calendar-style .el-calendar-table .el-calendar-day) {
  height: calc((100vh - 520px) / 6);
  padding: 0 8px;
}

:deep(.calendar-style .el-calendar-table) {
  padding-bottom: 0;
}

:deep(.calendar-style .el-calendar__body) {
  padding-bottom: 0;
}
</style>
