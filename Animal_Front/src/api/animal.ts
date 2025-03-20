import axios from "../utils/request";
import { Result } from "./response.interface.ts";

export class AnimalsApi {
  //获取所有动物信息
  async getAnimalInformationsApi(): Promise<Result> {
    const { data } = await axios.get("animals/");
    return data;
  }

  //创建动物信息
  async createAnimalInformationApi(AnimalInfo: any): Promise<Result> {
    const { data } = await axios.post("animals/", AnimalInfo);
    return data;
  }

  //获取特定id的动物信息
  async getAnimalDetailApi(animal_id: string): Promise<Result> {
    const { data } = await axios.get(`animals/${animal_id}/`);
    return data;
  }

  //更新特定id的动物信息
  async updateAnimalInformationApi(
    animal_id: string,
    AnimalInfo: any
  ): Promise<Result> {
    const { data } = await axios.post(
      `animals/update/${animal_id}/`,
      AnimalInfo
    );
    return data;
  }

  //删除特定id的动物信息
  async deleteAnimalInformationApi(animal_id: string): Promise<Result> {
    const { data } = await axios.post(`animals/delete/${animal_id}/`);
    return data;
  }

  //统计不同状态的动物数量
  async countAnimalsByStatusApi(): Promise<Result> {
    const { data } = await axios.get("animals/stats/");
    return data;
  }

  //上传动物图片
  async uploadAnimalPictureApi(animal_id: string, file: any): Promise<Result> {
    const { data } = await axios.post(`animals/${animal_id}/upload/`, file);
    return data;
  }
}
export default new AnimalsApi();
