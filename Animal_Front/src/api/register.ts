import axios from "../utils/request";
import { Result } from "./response.interface.ts";

export class UserRegister {
  // 普通用户注册接口
  async common_userRegisterApi(userInfo: any): Promise<Result> {
    const { data } = await axios.post("common_userRegister/", userInfo);
    return data;
  }
  // 管理员注册接口
  async adminRegisterApi(teacherInfo: any): Promise<Result> {
    const { data } = await axios.post("adminRegister/", teacherInfo);
    return data;
  }
}
export default new UserRegister();
