<template>
  <div class="task-listing-main-box">
    <!-- 任务列表标题 -->
    <div class="common-module-header-box">
      <el-icon>
        <Notebook />
      </el-icon>
      <span style="margin-left: 10px">任务列表</span>
      <!-- 新增任务按钮，仅管理员可见 -->
      <el-button
        v-if="userRole === 'Admin'"
        type="primary"
        @click="handleOpenCreateDialog"
        style="margin-left: 20px"
      >
        新增任务
      </el-button>
    </div>
    <!-- 查询框 -->
    <div class="common-module-query-box">
      <div class="module-query-item">
        <span class="module-query-item-title">任务标题: </span>
        <el-input
          v-model="queryInfo.title"
          placeholder="请输入任务标题"
          style="width: 220px"
          clearable
        />
      </div>
      <div class="module-query-item">
        <span class="module-query-item-title">任务状态: </span>
        <el-select
          v-model="queryInfo.status"
          placeholder="请选择任务状态"
          style="width: 240px"
          clearable
        >
          <el-option key="1" label="未被接取" value="未被接取" />
          <el-option key="2" label="进行中" value="进行中" />
          <el-option key="3" label="已完成，待确认" value="已完成，待确认" />
          <el-option key="4" label="确认完成" value="确认完成" />
          <el-option key="5" label="被驳回" value="被驳回" />
        </el-select>
      </div>
      <div class="module-query-item-btn">
        <el-button type="primary" @click="handleQuery">
          <Search class="common-btn-icon-style" />
          查 询
        </el-button>
      </div>
    </div>
    <!-- 任务表格 -->
    <div class="task-listing-table-box">
      <el-table
        border
        stripe
        size="small"
        :data="tableData"
        show-overflow-tooltip
        class="common-table-base-style"
        header-cell-class-name="table-header-row-style"
      >
        <el-table-column
          fixed
          type="index"
          align="center"
          width="60"
          label="序号"
        />
        <el-table-column
          fixed
          prop="title"
          label="任务标题"
          align="center"
          width="150"
        />
        <el-table-column
          prop="status"
          label="任务状态"
          align="center"
          width="120"
        >
          <template #default="scope">
            <el-tag
              size="small"
              v-if="scope['row']['status'] === '未被接取'"
              type="info"
            >
              未被接取
            </el-tag>
            <el-tag
              size="small"
              v-else-if="scope['row']['status'] === '进行中'"
              type="warning"
            >
              进行中
            </el-tag>
            <el-tag
              size="small"
              v-else-if="scope['row']['status'] === '已完成，待确认'"
              type="success"
            >
              已完成，待确认
            </el-tag>
            <el-tag
              size="small"
              v-else-if="scope['row']['status'] === '确认完成'"
              type="success"
            >
              确认完成
            </el-tag>
            <el-tag size="small" v-else type="danger"> 被驳回 </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="created_at"
          label="创建时间"
          align="center"
          width="180"
        />
        <el-table-column
          prop="deadline"
          label="截止时间"
          align="center"
          width="180"
        />
        <el-table-column :resizable="false" />
        <el-table-column
          fixed="right"
          label="操 作"
          align="center"
          width="270"
          :resizable="false"
        >
          <template #default="scope">
            <el-button
              link
              size="small"
              type="primary"
              :icon="Info"
              @click="handleOpenDetailDialog(scope['row'])"
            >
              详情
            </el-button>
            <el-divider direction="vertical" />

            <!-- 管理员编辑按钮 -->
            <el-button
              v-if="userRole === 'Admin'"
              link
              size="small"
              type="warning"
              :icon="SquarePen"
              @click="handleOpenEditDialog(scope['row'])"
            >
              编辑
            </el-button>
            <!-- 普通用户无编辑按钮 -->
            <el-divider v-if="userRole === 'Admin'" direction="vertical" />
            <el-button
              link
              size="small"
              type="danger"
              :icon="Trash2"
              @click="handleDelete(scope['row']['task_id'])"
            >
              删除
            </el-button>

            <el-divider v-if="userRole === 'Admin'" direction="vertical" />
            <el-button
              link
              size="small"
              type="success"
              :icon="Navigation"
              :disabled="
                scope['row']['is_published'] &&
                scope['row']['status'] !== '已完成待确定'
              "
              @click="handleButtonClick(scope['row'])"
            >
              {{ getButtonText(scope["row"]) }}
            </el-button>

            <el-divider direction="vertical" />
            <!-- 普通用户接取任务按钮 -->
            <el-button
              v-if="
                scope['row']['status'] === '未被接取' &&
                userRole === 'Common_user'
              "
              link
              size="small"
              type="success"
              :icon="Check"
              @click="handleTakeTask(scope['row']['task_id'])"
            >
              接取任务
            </el-button>
            <el-divider
              v-if="
                scope['row']['status'] === '未被接取' &&
                userRole === 'Common_user'
              "
              direction="vertical"
            />
            <!-- 普通用户完成任务按钮 -->
            <el-button
              v-if="
                ['进行中', '被驳回'].includes(scope['row']['status']) &&
                userRole === 'Common_user'
              "
              link
              size="small"
              type="success"
              :icon="Check"
              @click="handleCompleteTask(scope['row']['task_id'])"
            >
              完成任务
            </el-button>
            <el-divider
              v-if="
                ['进行中', '被驳回'].includes(scope['row']['status']) &&
                userRole === 'Common_user'
              "
              direction="vertical"
            />
            <!-- 管理员确认完成按钮 -->
            <el-button
              v-if="
                scope['row']['status'] === '已完成，待确认' &&
                userRole === 'Admin'
              "
              link
              size="small"
              type="success"
              :icon="Check"
              @click="handleConfirmTask(scope['row']['task_id'])"
            >
              确认完成
            </el-button>
            <el-divider
              v-if="
                scope['row']['status'] === '已完成，待确认' &&
                userRole === 'Admin'
              "
              direction="vertical"
            />
            <!-- 管理员驳回任务按钮 -->
            <el-button
              v-if="scope['row']['status'] === '进行中' && userRole === 'Admin'"
              link
              size="small"
              type="danger"
              :icon="X"
              @click="handleRejectTask(scope['row']['task_id'])"
            >
              驳回任务
            </el-button>
          </template>
        </el-table-column>
        <template #empty>
          <el-image
            style="width: 300px; opacity: 0.8"
            src="/src/images/noData.png"
            fit="cover"
          />
        </template>
      </el-table>
      <common-pagination
        :handle-current-change="handleCurrentChange"
        :page-size="pageSize"
        :table-page-total="tablePageTotal"
      />
    </div>
    <!-- 详情弹窗 -->
    <el-dialog
      width="800"
      title="任务详情"
      draggable
      destroy-on-close
      v-model="detailDialogVisible"
      :close-on-click-modal="false"
    >
      <div class="task-detail-box">
        <div class="detail-tag-box detail-common">
          <el-tag style="margin-right: 10px">
            <el-icon><Tag /></el-icon>
            {{ detailData["status"] }}
          </el-tag>
        </div>
        <div class="detail-common detail-topic-box">
          <span style="font-weight: bolder">任务标题：</span>
          <span style="margin-top: 10px; letter-spacing: 1px">{{
            detailData["title"]
          }}</span>
        </div>
        <div class="detail-common detail-description-box">
          <span style="font-weight: bolder">任务描述：</span>
          <span style="margin-top: 10px; letter-spacing: 1px">{{
            detailData["description"]
          }}</span>
        </div>
        <div class="detail-common detail-base-info-box">
          <div class="base-info">
            <div class="base-info-item">
              <span style="margin-right: 10px">创建时间：</span>
              <span>{{ detailData["created_at"] }}</span>
            </div>
            <div class="base-info-item">
              <span style="margin-right: 10px">截止时间：</span>
              <span>{{ detailData["deadline"] }}</span>
            </div>
            <div class="base-info-item">
              <span style="margin-right: 10px">任务发布者：</span>
              <span>{{ detailData["task_publisher_id"] }}</span>
            </div>
            <div class="base-info-item">
              <span style="margin-right: 10px">任务接取人：</span>
              <span>{{ detailData["task_taker_id"] }}</span>
            </div>
            <div class="base-info-item">
              <span style="margin-right: 10px">积分：</span>
              <span>{{ detailData["points"] }}</span>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
    <!-- 编辑弹窗 -->
    <el-dialog
      width="800"
      title="编辑任务信息"
      draggable
      destroy-on-close
      v-model="editDialogVisible"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      @close="handleCloseEditDialog(formRef)"
    >
      <el-form :model="formData" ref="formRef">
        <el-form-item
          label="任务标题"
          :label-width="formLabelWidth"
          prop="title"
          required
        >
          <el-input
            v-model="formData.title"
            placeholder="请输入任务标题"
            clearable
          />
        </el-form-item>
        <el-form-item
          label="任务描述"
          :label-width="formLabelWidth"
          prop="description"
          required
        >
          <el-input
            v-model="formData.description"
            placeholder="请输入任务描述"
            clearable
          />
        </el-form-item>
        <el-form-item
          label="任务状态"
          :label-width="formLabelWidth"
          prop="status"
          required
        >
          <el-select v-model="formData.status" placeholder="请选择任务状态">
            <el-option label="未被接取" value="未被接取" key="未被接取" />
            <el-option label="进行中" value="进行中" key="进行中" />
            <el-option
              label="已完成，待确认"
              value="已完成，待确认"
              key="已完成，待确认"
            />
            <el-option label="确认完成" value="确认完成" key="确认完成" />
            <el-option label="被驳回" value="被驳回" key="被驳回" />
          </el-select>
        </el-form-item>
        <el-form-item
          label="截止时间"
          :label-width="formLabelWidth"
          prop="deadline"
          required
        >
          <el-date-picker
            v-model="formData.deadline"
            type="datetime"
            placeholder="请选择截止时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DDTHH:mm:ss"
            :disabled-date="disabledDate"
          />
        </el-form-item>
        <el-form-item
          label="积分"
          :label-width="formLabelWidth"
          prop="points"
          required
        >
          <el-input
            v-model="formData.points"
            placeholder="请输入积分"
            clearable
            type="number"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="handleCloseEditDialog(formRef)" :icon="Ban"
            >取 消</el-button
          >
          <el-button
            type="primary"
            @click="handleSubmitEditTask(formRef)"
            :icon="Send"
            >提 交</el-button
          >
        </div>
      </template>
    </el-dialog>
    <!-- 新增任务弹窗 -->
    <el-dialog
      width="800"
      title="新增任务信息"
      draggable
      destroy-on-close
      v-model="createDialogVisible"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      @close="handleCloseCreateDialog(formRef)"
    >
      <el-form :model="createFormData" ref="formRef">
        <el-form-item
          label="任务标题"
          :label-width="formLabelWidth"
          prop="title"
          required
        >
          <el-input
            v-model="createFormData.title"
            placeholder="请输入任务标题"
            clearable
          />
        </el-form-item>
        <el-form-item
          label="任务描述"
          :label-width="formLabelWidth"
          prop="description"
          required
        >
          <el-input
            v-model="createFormData.description"
            placeholder="请输入任务描述"
            clearable
          />
        </el-form-item>
        <el-form-item
          label="任务状态"
          :label-width="formLabelWidth"
          prop="status"
          required
        >
          <el-select
            v-model="createFormData.status"
            placeholder="请选择任务状态"
          >
            <el-option label="未被接取" value="未被接取" key="未被接取" />
            <el-option label="进行中" value="进行中" key="进行中" />
            <el-option
              label="已完成，待确认"
              value="已完成，待确认"
              key="已完成，待确认"
            />
            <el-option label="确认完成" value="确认完成" key="确认完成" />
            <el-option label="被驳回" value="被驳回" key="被驳回" />
          </el-select>
        </el-form-item>
        <el-form-item
          label="截止时间"
          :label-width="formLabelWidth"
          prop="deadline"
          required
        >
          <el-date-picker
            v-model="createFormData.deadline"
            type="datetime"
            placeholder="请选择截止时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DDTHH:mm:ss"
          />
        </el-form-item>
        <el-form-item
          label="积分"
          :label-width="formLabelWidth"
          prop="points"
          required
        >
          <el-input
            v-model="createFormData.points"
            placeholder="请输入积分"
            clearable
            type="number"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="handleCloseCreateDialog(formRef)" :icon="Ban"
            >取 消</el-button
          >
          <el-button
            type="primary"
            @click="handleSubmitCreateTask(formRef)"
            :icon="Send"
            >提 交</el-button
          >
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, reactive, ref } from "vue";
import {
  Notebook,
  Search,
  Info,
  SquarePen,
  Trash2,
  Tag,
  Ban,
  Send,
  Check,
  X,
  Navigation,
} from "lucide-vue-next";
import { ElMessage, ElMessageBox } from "element-plus";
import CommonPagination from "../../components/CommonPagination.vue";
import { TasksApi } from "../../api"; // 引入新的 API 模块
import { getCookie } from "../../utils/cookie";

// 获取用户ID和角色
const userInfo = getCookie("UserInfo") ? JSON.parse(getCookie("UserInfo")) : {};
const userId = userInfo.userId;
const userRole = localStorage.getItem("ROLE");

// 查询条件
const queryInfo = reactive({
  title: null,
  status: null,
});
// 处理查询
const handleQuery = () => {
  getTaskList();
};

// 存储表格数据
const tableData = ref<any[]>([]);
// 当前页
const currentPage = ref(1);
// 每页数量
const pageSize = ref(50);
// 数据总数
const tablePageTotal = ref(0);
// 获取任务列表数据
const getTaskList = async () => {
  try {
    TasksApi.adminGetTaskByStatusAndTitleApi(
      queryInfo.status || "",
      queryInfo.title || ""
    ).then((response) => {
      if (response.code === 200) {
        tableData.value = response.data;
        tablePageTotal.value = response.data.length;

        console.log(tableData.value, tablePageTotal.value);
      } else {
        ElMessage.error(response.msg);
      }
    });
  } catch (error) {
    ElMessage.error("获取任务列表失败");
  }
};

// 处理分页时当前页的变更事件
const handleCurrentChange = (val: number) => {
  currentPage.value = val;
  getTaskList();
};

onMounted(() => {
  getTaskList();
});

// 控制详情Dialog是否可见
const detailDialogVisible = ref(false);
// 存储详情数据信息
const detailData = ref<any>(null);
// 处理打开详情Dialog
const handleOpenDetailDialog = (itemData: any) => {
  detailData.value = itemData;
  detailDialogVisible.value = true;
};

// 处理删除任务
const handleDelete = async (taskId: string) => {
  ElMessageBox.confirm("您确定要删除这个任务吗？", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
    center: true,
  })
    .then(async () => {
      try {
        const response = await TasksApi.adminDeleteTaskApi(taskId);
        if (response.code === 200) {
          ElMessage.success("删除任务成功！");
          getTaskList();
        } else {
          ElMessage.error(response.msg);
        }
      } catch (error) {
        ElMessage.error("删除任务失败");
      }
    })
    .catch(() => {
      ElMessage.info("取消删除!");
    });
};

//处理发布任务
const handlePublishTask = async (taskId: string) => {
  ElMessageBox.confirm("您确定要发布这个任务吗？", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    center: true,
  })
    .then(async () => {
      try {
        const response = await TasksApi.adminPublishTaskApi(taskId);
        if (response.code === 200) {
          ElMessage.success("发布任务成功！");
          getTaskList();
        } else {
          ElMessage.error(response.msg);
        }
      } catch (error) {
        ElMessage.error("发布任务失败");
      }
    })
    .catch(() => {
      ElMessage.info("取消发布!");
    });
};

// 控制编辑任务信息Dialog是否可见
const editDialogVisible = ref(false);
// Dialog中Form Label的通用宽度
const formLabelWidth = "100px";
// 新增任务表单的Ref
const formRef = ref<any>();

// 任务 FormData
const formData = ref<any>({});

// 处理关闭编辑任务Dialog
const handleCloseEditDialog = (formEl: any) => {
  formData.value = {};
  formEl.resetFields();
  editDialogVisible.value = false;
};

// 处理打开编辑任务信息Dialog
const handleOpenEditDialog = (item: any) => {
  editDialogVisible.value = true;
  formData.value = {
    ...item,
  };
};
// 提交编辑任务
const handleSubmitEditTask = async (formEl: any) => {
  formEl.validate(async (result: boolean) => {
    if (!result) {
      ElMessage.warning("请输入完整的信息！");
      return;
    }
    try {
      const response = await TasksApi.adminUpdateTaskInformationApi(
        formData.value.task_id,
        formData.value
      );
      if (response.code === 200) {
        ElMessage.success("编辑成功！");
        getTaskList();
        editDialogVisible.value = false;
      } else {
        ElMessage.error(response.msg);
      }
    } catch (error) {
      ElMessage.error("编辑任务失败");
    }
  });
};

// 用户接取任务
const handleTakeTask = async (taskId: string) => {
  try {
    const response = await TasksApi.userTakeTaskApi(taskId);
    if (response.code === 200) {
      ElMessage.success("任务接取成功");
      getTaskList();
    } else {
      ElMessage.error(response.msg);
    }
  } catch (error) {
    ElMessage.error("任务接取失败");
  }
};

// 用户完成任务
const handleCompleteTask = async (taskId: string) => {
  try {
    const response = await TasksApi.userCompleteTaskApi(taskId);
    if (response.code === 200) {
      ElMessage.success("任务完成，等待管理员确认");
      getTaskList();
    } else {
      ElMessage.error(response.msg);
    }
  } catch (error) {
    ElMessage.error("任务完成失败");
  }
};

// 管理员确认任务完成
const handleConfirmTask = async (taskId: string) => {
  try {
    const response = await TasksApi.adminConfirmCompleteTaskApi(taskId);
    if (response.code === 200) {
      ElMessage.success("任务确认完成，积分已添加");
      getTaskList();
    } else {
      ElMessage.error(response.msg);
    }
  } catch (error) {
    ElMessage.error("任务确认失败");
  }
};

// 管理员驳回任务
const handleRejectTask = async (taskId: string) => {
  try {
    const response = await TasksApi.adminRejectTaskApi(taskId);
    if (response.code === 200) {
      ElMessage.success("任务成功被驳回");
      getTaskList();
    } else {
      ElMessage.error(response.msg);
    }
  } catch (error) {
    ElMessage.error("任务驳回失败");
  }
};

// 控制新增任务Dialog是否可见
const createDialogVisible = ref(false);
// 新增任务表单数据
const createFormData = ref<any>({
  status: "未被接取",
});

// 处理打开新增任务Dialog
const handleOpenCreateDialog = () => {
  createDialogVisible.value = true;
};

// 处理关闭新增任务Dialog
const handleCloseCreateDialog = (formEl: any) => {
  createFormData.value = {
    status: "未被接取",
  };
  formEl.resetFields();
  createDialogVisible.value = false;
};

// 提交新增任务
const handleSubmitCreateTask = async (formEl: any) => {
  formEl.validate(async (result: boolean) => {
    if (!result) {
      ElMessage.warning("请输入完整的信息！");
      return;
    }
    try {
      const response = await TasksApi.adminCreateTaskApi(createFormData.value);
      if (response.code === 200) {
        ElMessage.success("新增任务成功！");
        getTaskList();
        createDialogVisible.value = false;
      } else {
        ElMessage.error(response.msg);
      }
    } catch (error) {
      ElMessage.error("新增任务失败");
    }
  });
};

const disabledDate = (time: any) => {
  // 将当前时间减去 86400000 毫秒（即一天），确保可以选择今天及之后的时间
  return time.getTime() < Date.now() - 86400000;
};

const handleButtonClick = (task:any) => {
  if (!task.is_published) {
    handlePublishTask(task.task_id);
  } else if (task.status === '已完成待确定') {
    // 这里可以添加确认/驳回的逻辑
    console.log('执行确认/驳回操作');
  }
};

const getButtonText = (task:any) => {
  if (!task.is_published) {
    return '发布';
  } else if (task.status === '已完成，待确认') {
    return '确认/驳回';
  }
  return '已发布';
};
</script>

<style scoped lang="scss">
@import "../../style.scss";

@include tableHeaderStyle;

.task-listing-main-box {
  @include baseFlexStyle {
    flex-direction: column;
  }
}

.task-listing-table-box {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 260px);
}
</style>
