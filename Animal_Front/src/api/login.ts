import axios from '../utils/request'
import { Result } from "./response.interface.ts";


export class UserLogin {
  // 普通用户用户登录接口
  async common_userLoginApi(common_userInfo: any): Promise<Result> {
    const { data } = await axios.post('common_userLogin/', common_userInfo)
    return data
  }

  // 管理员用户登录接口
  async adminLoginApi(adminInfo: any): Promise<Result> {
    const { data } = await axios.post('adminLogin/', adminInfo)
    return data
  }

  // 管理员用户修改密码接口
  async adminChangePasswordApi(userId: string, pwdInfo: any): Promise<Result> {
    const { data } = await axios.put(`adminChangePassword/${userId}/`, pwdInfo)
    return data
  }

  // 普通用户用户修改密码接口
  async common_userChangePasswordApi(userId: string, pwdInfo: any): Promise<Result> {
    const { data } = await axios.put(`common_userChangePassword/${userId}/`, pwdInfo)
    return data
  }
}

export default new UserLogin()
