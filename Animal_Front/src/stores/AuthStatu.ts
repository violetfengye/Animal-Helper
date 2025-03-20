import { defineStore } from 'pinia';

export const useUserStatu = defineStore('UserStatu',{
    // 真正存储数据的地方
    state(){
      return {
        role: "Common_user"
      }
    }
  })