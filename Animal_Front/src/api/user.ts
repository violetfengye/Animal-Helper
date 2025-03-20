import axios from '../utils/request'
import { Result } from "./response.interface.ts";


export class User {
  // 获取学生信息列表接口
  async getCommon_usersApi(querySet: object, currentPage: number, pageSize:number): Promise<Result> {
    const { data } = await axios.get('common_user/', {
      params: { ...querySet, currentPage, pageSize }
    })
    return data
  }

  // 批量激活学生接口
  async batchActiveCommon_usersApi(ids: string[]): Promise<Result> {
    const { data } = await axios.post('common_userBatchActivation/', { ids })
    return data
  }

  // 新增学生信息接口
  async createCommon_userApi(common_userInfo: any): Promise<Result> {
    const { data } = await axios.post('common_user/', { ...common_userInfo })
    return data
  }

  // 编辑学生信息接口
  async editCommon_userApi(common_userInfo: any): Promise<Result> {
    const { data } = await axios.put(`common_user/${common_userInfo['id']}`, { ...common_userInfo })
    return data
  }

  // 删除学生信息接口
  async deleteCommon_userApi(id: string): Promise<Result> {
    const { data } = await axios.delete(`common_user/${id}`)
    return data
  }

  // 获取教师信息列表接口
  async getAdminsApi(querySet: object, currentPage: number, pageSize:number): Promise<Result> {
    const { data } = await axios.get('admin/', {
      params: { ...querySet, currentPage, pageSize }
    })
    return data
  }

  // 删除教师信息接口
  async deleteAdminApi(id: string): Promise<Result> {
    const { data } = await axios.delete(`admin/${id}`)
    return data
  }

  // 新增教师信息接口
  async createAdminApi(adminInfo: any): Promise<Result> {
    const { data } = await axios.post('admin/', { ...adminInfo })
    return data
  }

  // 编辑教师信息接口
  async editAdminApi(adminInfo: any): Promise<Result> {
    const { data } = await axios.put(`admin/${adminInfo['id']}`, { ...adminInfo })
    return data
  }
}

export default new User()
