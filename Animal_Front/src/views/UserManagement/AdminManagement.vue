<template>
  <div class="admin-main-box">
    <div class="common-module-header-box">
      <el-icon><Users /></el-icon>
      <span style="margin-left: 10px">管理员管理</span>
    </div>
    <div class="common-module-query-box">
      <div class="module-query-item">
        <span class="module-query-item-title">管理员编号: </span>
        <el-input v-model="queryInfo.admin_id" placeholder="请输入管理员编号" style="width: 220px" clearable/>
      </div>
      <div class="module-query-item">
        <span class="module-query-item-title">管理员姓名: </span>
        <el-input v-model="queryInfo.name" placeholder="请输入管理员姓名" style="width: 220px" clearable/>
      </div>
      <div class="module-query-item-btn">
        <el-button type="primary" @click="getAdmins">
          <Search class="common-btn-icon-style"/>
          查 询
        </el-button>
      </div>
    </div>
    <div class="common-module-opts-box">
      <el-button color="#42b883" style="color: #fff" @click="handleOpenDialog('C')">
        <Plus class="common-btn-icon-style"/>
        新 增
      </el-button>
    </div>
    <div class="papers-table-box">
      <el-table
          border
          stripe
          size="small"
          :data="tableData"
          show-overflow-tooltip
          class="common-table-base-style"
          header-cell-class-name="table-header-row-style"
      >
        <el-table-column fixed type="index" align="center" width="60" label="序号"/>
        <el-table-column fixed prop="admin_id" label="管理员编号" align="center" width="180"/>
        <el-table-column prop="name" label="姓名" align="center" width="180"/>
        <el-table-column prop="username" label="登录账号" align="center" width="180"/>
        <el-table-column prop="gender" label="性别" align="center" width="120">
          <template #default="scope">
            <span v-if="scope['row']['gender'] === 'male'">男</span>
            <span v-else>女</span>
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="激活状态" align="center" width="120">
          <template #default="scope">
            <el-tag size="small" v-if="scope['row']['is_active']" type="success">
              <el-icon><Check /></el-icon>
              已激活
            </el-tag>
            <el-tag size="small" v-else type="danger">
              <el-icon><X /></el-icon>
              未激活
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="phone" label="电话" align="center" width="180">
          <template #default="scope">
            <span v-if="scope['row']['phone']">{{ scope['row']['phone'] }}</span>
            <span v-else>--</span>
          </template>
        </el-table-column>
        <el-table-column prop="email" label="邮箱" align="center" width="180">
          <template #default="scope">
            <span v-if="scope['row']['email']">{{ scope['row']['email'] }}</span>
            <span v-else>--</span>
          </template>
        </el-table-column>
        <el-table-column prop="grade" label="年级" align="center" width="180">
          <template #default="scope">
            <span v-if="scope['row']['grade']">{{ scope['row']['grade'] }}</span>
            <span v-else>--</span>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" align="center" width="180"/>
        <el-table-column prop="updated_at" label="更新时间" align="center" width="180"/>
        <el-table-column :resizable="false"/>
        <el-table-column fixed="right" label="操 作" align="center" width="180" :resizable="false">
          <template #default="scope">
            <el-button
                link
                size="small"
                type="warning"
                :icon="SquarePen"
                @click="handleOpenDialog('E', scope['row'])"
            >
              编辑
            </el-button>
            <el-divider direction="vertical"/>
            <el-button link size="small" type="danger" :icon="Trash2" @click="handleDelete(scope['row']['id'])">
              删除
            </el-button>
          </template>
        </el-table-column>
        <template #empty>
          <el-image style="width: 300px;opacity: 0.8" src="/src/images/noData.png" fit="cover"/>
        </template>
      </el-table>
      <common-pagination
          :handle-current-change="handleCurrentChange"
          :table-page-total="tablePageTotal"
          :page-size="pageSize"
      />
    </div>
    <el-dialog
        width="800"
        :title="optType === 'C' ? '新增管理员用户' : '编辑管理员用户'"
        draggable
        destroy-on-close
        v-model="dialogVisible"
        :close-on-click-modal="false"
        :close-on-press-escape="false"
        @close="handleClose(formRef)"
    >
      <el-form :model="formData" ref="formRef">
        <el-form-item label="管理员编号" :label-width="formLabelWidth" prop="admin_id" required>
          <el-input v-model="formData.admin_id" placeholder="请输入管理员编号（唯一）" clearable/>
        </el-form-item>
        <el-form-item label="管理员姓名" :label-width="formLabelWidth" prop="name" required>
          <el-input v-model="formData.name" placeholder="请输入管理员姓名" clearable/>
        </el-form-item>
        <el-form-item label="登录账号" :label-width="formLabelWidth" prop="username">
          <el-input v-model="formData.username" placeholder="请输入登录账号（若为空，默认管理员编号为登录账号）" clearable/>
        </el-form-item>
        <el-form-item label="性别" :label-width="formLabelWidth" prop="gender" required>
          <el-select v-model="formData.gender" placeholder="请选择性别">
            <el-option label="男" value="male"/>
            <el-option label="女" value="female"/>
          </el-select>
        </el-form-item>
        <el-form-item label="电话" :label-width="formLabelWidth" prop="phone">
          <el-input v-model="formData.phone" placeholder="请输入电话" clearable/>
        </el-form-item>
        <el-form-item label="邮箱" :label-width="formLabelWidth" prop="email">
          <el-input v-model="formData.email" placeholder="请输入邮箱" clearable/>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false" :icon="Ban">取 消</el-button>
          <el-button type="primary" @click="handleSubmit(formRef)" :icon="Send">提 交</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import {onMounted, reactive, ref} from 'vue'
import { User } from "../../api/index.ts"
import {ElMessage, ElMessageBox} from "element-plus";
import {getCookie} from "../../utils/cookie.ts";
import type {FormInstance} from 'element-plus'
import {Users, Plus, Search, SquarePen, Trash2, X, Check, Ban, Send} from "lucide-vue-next";
import CommonPagination from "../../components/CommonPagination.vue";

// 获取UserID
const userId = JSON.parse(getCookie('UserInfo')).userId

// 查询条件
const queryInfo = reactive({
  name: null,
  admin_id: null,
  is_deleted: false,
  is_active: null
})

// 存储表格数据
const tableData: any = ref([])
// 当前页
const currentPage = ref(1)
// 每页数量
const pageSize = ref(50)
// 数据总数
const tablePageTotal = ref(0)

// 处理分页时当前页的变更事件
const handleCurrentChange = (val: number) => {
  currentPage.value = val
  getAdmins()
}

// 获取管理员信息
const getAdmins = () => {
  User.getAdminsApi(queryInfo, currentPage.value, pageSize.value).then(response => {
    if (response.code !== 200) {
      ElMessage.error(response.msg)
      return
    } else {
      tableData.value = response.data.data
      tablePageTotal.value = response.data.total
    }
  })
}

onMounted(() => {
  getAdmins()
})

// 处理删除管理员信息
const handleDelete = (rowId: string) => {
  ElMessageBox.confirm(
      '您确定要删除吗？',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        center: true,
      }
  ).then(() => {
    User.deleteAdminApi(rowId).then(response => {
      if (response.code !== 200) {
        ElMessage.error(response.msg)
        return
      }
      ElMessage.success('删除成功！')
      getAdmins()
    })
  }).catch(() => {
    ElMessage.info('取消删除')
  })
}

// Dialog中Form Label的通用宽度
const formLabelWidth = '100px'
// 控制新增&编辑用户信息Dialog
const dialogVisible = ref(false)
// 控制是新增还是编辑
const optType = ref('C')
// 处理打开新增&编辑用户信息Dialog
const handleOpenDialog = (opt: string, itemData?: any) => {
  if (opt === 'E') {
    formData.value = itemData
  }
  optType.value = opt
  dialogVisible.value = true
}
// 新增管理员表单的Ref
const formRef = ref<FormInstance>()
// FormData 初始化
const initFormData = {
  admin_id: '',
  name: '',
  username: '',
  password: '123456',
  role: 'admin',
  gender: '',
  phone: '',
  email: '',
  is_active: true,
  created_user: userId,
  updated_user: userId
}
// 试题 FormData
const formData = ref(initFormData)
// 处理关闭Dialog回调函数
const handleClose = (createFormEl: any) => {
  formData.value = initFormData
  createFormEl.resetFields()
  dialogVisible.value = false
}

// 处理提交管理员信息
const handleSubmit = async (createFormEl: any) => {
  // 数据校验
  createFormEl.validate(async (result: boolean) => {
    if (!result) {
      ElMessage.warning('请输入完整的管理员信息后重新提交！')
      return
    }
    try {
      if (!formData.value.username) {
        formData.value.username = formData.value.admin_id
      }
      const response = optType.value === 'C'
          ? await User.createAdminApi(formData.value)
          : await User.editAdminApi({...formData.value, updated_user: userId})
      if (response.code !== 200) {
        ElMessage.error(response.msg)
        return
      }
      ElMessage.success(optType.value === 'C' ? '新增管理员信息成功！' : '编辑管理员信息成功！')
      getAdmins()
      dialogVisible.value = false
    } catch (error) {
      console.error('An error occurred:', error)
    }
  })
}
</script>

<style scoped lang="scss">
@import "../../style.scss";

@include tableHeaderStyle;

.admin-main-box {
  @include baseFlexStyle {
    flex-direction: column;
  }
}
</style>
