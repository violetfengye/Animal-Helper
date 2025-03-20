import { createRouter, createWebHistory } from "vue-router";
import { getCookie } from "../utils/cookie";
import { pa } from "element-plus/es/locales.mjs";


const routers: any = [
  {
    path: "/login",
    component: ()=>import("../views/Login/index.vue"),
  },
  {
    path: "/register",
    component: ()=>import("../views/Register/index.vue"),
  },
  {
    path: "/",
    component: ()=>import("../components/Container.vue"),
    redirect: "/homepage",
    children: [
      {
        path: "/homepage",
        component: ()=>import("../views/HomePage/index.vue"),
      },
      {
        path: "/animals",
        component: ()=>import("../views/AnimalInfo/index.vue"),
      },
      // {
      //   path: "/common_user_management",
      //   component: ()=>import("../views/UserManagement/CommonUserManagement.vue"),
      // },
      // {
      //   pay: "/admin_management",
      //   component: ()=>import("../views/UserManagement/AdminManagement.vue"),
      // },
      {
        path:"/tasksInformation",
        component: ()=>import("../views/TaskInfo/index.vue"),
      },
      
    ],
  },
];

export const router = createRouter({
  history: createWebHistory(),
  routes: routers,
});

// 增加路由守卫，确保登录态后跳转页面
// 使用 router.beforeEach 注册一个全局前置守卫，对所有路由导航进行拦截
router.beforeEach((to, _, next) => {
  // 用户必须登录才能访问任何页面
  const isAuthenticated = localStorage.getItem("TOKEN");
  const userInfo = getCookie("UserInfo");
  if (
    to.path !== "/login" &&
    to.path !== "/register" &&
    (!isAuthenticated || !userInfo)
  ) {
    next("/login"); // 如果用户未登录，将其重定向到登录页面
  } else {
    next(); // 如果用户已登录，继续路由导航
  }
});

export default router;
