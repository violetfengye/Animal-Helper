<template>
    <div class="animal-management-container">
        <!-- 搜索框 -->
        <div class="search-box">
            <el-input v-model="searchQuery" placeholder="搜索动物名称" @keyup.enter.native="searchAnimals" clearable />
            <el-input v-model="schoolQuery" placeholder="按学校筛选" @keyup.enter.native="filterBySchool" clearable />
            <el-button @click="searchAnimals" type="primary">搜索</el-button>
            <el-button @click="filterBySchool" type="primary">按学校筛选</el-button>
            <el-button @click="openCreateDialog" type="success">创建动物信息</el-button>
        </div>

        <!-- 动物信息表格 -->
        <el-table :data="filteredAnimals" stripe border>
            <el-table-column prop="animal_id" label="动物编号" />
            <el-table-column prop="name" label="动物名" />
            <el-table-column prop="status" label="动物状态" />
            <el-table-column prop="school" label="所属学校" />
            <el-table-column prop="created_at_formatted" label="创建时间" />
            <el-table-column prop="updated_at_formatted" label="更新时间" />
            <el-table-column label="动物图片">
                <template slot-scope="scope">
                    <img :src="scope.row.img" alt="动物图片" style="max-width: 100px; max-height: 100px;" />
                </template>
            </el-table-column>
            <el-table-column label="操作">
                <template slot-scope="scope">
                    <el-button @click="openUpdateDialog(scope.row)" type="warning" size="small">编辑</el-button>
                    <el-button @click="deleteAnimal(scope.row.animal_id)" type="danger" size="small">删除</el-button>
                </template>
            </el-table-column>
        </el-table>

        <!-- 创建动物信息对话框 -->
        <el-dialog :visible.sync="createDialogVisible" title="创建动物信息">
            <el-form :model="newAnimal" label-width="120px">
                <el-form-item label="动物编号">
                    <el-input v-model="newAnimal.animal_id" />
                </el-form-item>
                <el-form-item label="动物名">
                    <el-input v-model="newAnimal.name" />
                </el-form-item>
                <el-form-item label="动物状态">
                    <el-input v-model="newAnimal.status" />
                </el-form-item>
                <el-form-item label="所属学校">
                    <el-input v-model="newAnimal.school" />
                </el-form-item>
                <el-form-item label="动物图片">
                    <el-input v-model="newAnimal.img" />
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="createDialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="createAnimal">确定</el-button>
                </span>
            </template>
        </el-dialog>

        <!-- 更新动物信息对话框 -->
        <el-dialog :visible.sync="updateDialogVisible" title="更新动物信息">
            <el-form :model="updateAnimal" label-width="120px">
                <el-form-item label="动物编号">
                    <el-input v-model="updateAnimal.animal_id" disabled />
                </el-form-item>
                <el-form-item label="动物名">
                    <el-input v-model="updateAnimal.name" />
                </el-form-item>
                <el-form-item label="动物状态">
                    <el-input v-model="updateAnimal.status" />
                </el-form-item>
                <el-form-item label="所属学校">
                    <el-input v-model="updateAnimal.school" />
                </el-form-item>
                <el-form-item label="动物图片">
                    <el-input v-model="updateAnimal.img" />
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="updateDialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="updateAnimalInfo">确定</el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue';
import {AnimalsApi} from '../../api';

// 所有动物数据
const animals = ref([]);

// 搜索框输入内容
const searchQuery = ref('');
const schoolQuery = ref('');

// 对话框显示状态
const createDialogVisible = ref(false);
const updateDialogVisible = ref(false);

// 新动物信息
const newAnimal = ref({
    animal_id: '',
    name: '',
    status: 'active',
    school: '',
    img: ''
});

// 待更新的动物信息
const updateAnimal = ref({
    animal_id: '',
    name: '',
    status: 'active',
    school: '',
    img: ''
});

// 过滤后的动物列表
const filteredAnimals = computed(() => {
    let result = animals.value;
    if (searchQuery.value) {
        result = result.filter(animal =>
            animal.name.includes(searchQuery.value)
        );
    }
    if (schoolQuery.value) {
        result = result.filter(animal =>
            animal.school.includes(schoolQuery.value)
        );
    }
    return result;
});

// 获取所有动物信息
const fetchAnimals = async () => {
    try {
        const response = await AnimalsApi.getAnimalInformationsApi();
        animals.value = response.data;
    } catch (error) {
        console.error('获取动物信息失败:', error);
    }
};

// 搜索函数
const searchAnimals = () => {
    // 触发过滤逻辑
};

// 按学校筛选函数
const filterBySchool = () => {
    // 触发过滤逻辑
};

// 打开创建对话框
const openCreateDialog = () => {
    createDialogVisible.value = true;
};

// 创建动物信息
const createAnimal = async () => {
    try {
        await AnimalsApi.createAnimalInformationApi(newAnimal.value);
        createDialogVisible.value = false;
        fetchAnimals();
    } catch (error) {
        console.error('创建动物信息失败:', error);
    }
};

// 打开更新对话框
const openUpdateDialog = (animal:any) => {
    updateAnimal.value = { ...animal };
    updateDialogVisible.value = true;
};

// 更新动物信息
const updateAnimalInfo = async () => {
    try {
        await AnimalsApi.updateAnimalInformationApi(updateAnimal.value.animal_id, updateAnimal.value);
        updateDialogVisible.value = false;
        fetchAnimals();
    } catch (error) {
        console.error('更新动物信息失败:', error);
    }
};

// 删除动物信息
const deleteAnimal = async (animal_id:any) => {
    try {
        await AnimalsApi.deleteAnimalInformationApi(animal_id);
        fetchAnimals();
    } catch (error) {
        console.error('删除动物信息失败:', error);
    }
};

// 初始化数据
fetchAnimals();
</script>

<style scoped>
.animal-management-container {
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.search-box {
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
}
</style>    