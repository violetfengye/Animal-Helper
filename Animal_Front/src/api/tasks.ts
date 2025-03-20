import axios from "../utils/request";
import { Result } from "./response.interface.ts";

export class TasksApi {
  //获取所有任务信息
  async getTasksApi(): Promise<Result> {
    const { data } = await axios.get("tasks/");
    return data;
  }

  //创建任务信息
  async adminCreateTaskApi(taskInfo: any): Promise<Result> {
    const { data } = await axios.post("tasks/", taskInfo);
    return data;
  }

  //获取特定id的任务信息
  async getTaskDetailApi(task_id: string): Promise<Result> {
    const { data } = await axios.get(`tasks/${task_id}/`);
    return data;
  }

  //更新特定id的任务信息
  async adminUpdateTaskInformationApi(
    task_id: string,
    TaskInfo: any
  ): Promise<Result> {
    const { data } = await axios.patch(`tasks/${task_id}/`, TaskInfo);
    return data;
  }

  //删除特定id的任务信息
  async adminDeleteTaskApi(task_id: string): Promise<Result> {
    const { data } = await axios.delete(`tasks/${task_id}/`);
    return data;
  }

  //用户接取任务，更新任务状态为进行中
  async userTakeTaskApi(task_id: string): Promise<Result> {
    const { data } = await axios.get(`tasks/${task_id}/take/`);
    return data;
  }

  //用户完成任务，更新任务状态为待确认
  async userCompleteTaskApi(task_id: string): Promise<Result> {
    const { data } = await axios.get(`tasks/${task_id}/complete/`);
    return data;
  }

  //任务确认完成
  async adminConfirmCompleteTaskApi(task_id: string): Promise<Result> {
    const { data } = await axios.get(`tasks/${task_id}/confirm-complete/`);
    return data;
  }
  //任务驳回
  async adminRejectTaskApi(task_id: string): Promise<Result> {
    const { data } = await axios.get(`tasks/${task_id}/reject/`);
    return data;
  }
  //获取指定用户所有任务
  async userGetTaskApi(user_id: string): Promise<Result> {
    const { data } = await axios.get(`user/${user_id}/tasks/`);
    return data;
  }
  //管理员发布任务
  async adminPublishTaskApi(task_id: string): Promise<Result> {
    const { data } = await axios.get(`tasks/publish/${task_id}/`);
    return data;
  }
  //根据状态和标题删选任务
  async adminGetTaskByStatusAndTitleApi(
    status?: string,
    title?: string
  ): Promise<Result> {
    let url = "tasks_filter/?";
    if (status) {
      url += `status=${status}&`;
    }
    if (title) {
      url += `title=${title}&`;
    }
    // 去掉最后一个多余的 '&'
    url = url.replace(/&$/, "");
    const { data } = await axios.get(url);
    return data;
  }
}
export default new TasksApi();
