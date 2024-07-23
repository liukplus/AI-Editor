import axios, { InternalAxiosRequestConfig, AxiosResponse } from "axios";
import { useUserStoreHook } from "@/store/modules/user";
import { ResultEnum } from "@/enums/ResultEnum";
import { TOKEN_KEY } from "@/enums/CacheEnum";

// 创建 axios 实例
const service = axios.create({
  timeout: 50000,
  headers:{"Content-Type":'multipart/form-data'}
});

// 请求拦截器
service.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const accessToken = localStorage.getItem(TOKEN_KEY);
    config.data.append("user_id",localStorage.getItem("user_id"));
    config.data.append("text_id",44);
    return config;
  },
  (error: any) => {
    return Promise.reject(error);
  }
);


// 导出 axios 实例
export default service;
